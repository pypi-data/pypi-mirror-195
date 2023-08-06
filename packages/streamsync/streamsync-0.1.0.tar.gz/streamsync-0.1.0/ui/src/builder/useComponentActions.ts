import {
	Core,
	BuilderManager,
	Component,
	ClipboardOperation,
} from "../streamsyncTypes";

export function useComponentActions(ss: Core, ssbm: BuilderManager) {
	function moveComponentUp(componentId: Component["id"]): void {
		const component = ss.getComponentById(componentId);
		if (!component) return;
		const position = component.position;
		if (position == 0) return;
		const parent = ss.getComponentById(component.parentId);
		if (!parent) return;

		const previousSibling = ss
			.getComponents(parent.id)
			.filter((c) => c.position == position - 1)[0];

		// MUTATIONS

		const transactionId = `move-up-${componentId}`;
		ssbm.openMutationTransaction(transactionId, `Move up`);
		ssbm.registerPreMutation(previousSibling);
		previousSibling.position++;
		ssbm.registerPostMutation(previousSibling);
		ssbm.registerPreMutation(component);
		component.position--;
		ssbm.registerPostMutation(component);
		ssbm.closeMutationTransaction(transactionId);
		ss.sendComponentUpdate();
	}

	function moveComponentDown(componentId: Component["id"]): void {
		const component = ss.getComponentById(componentId);
		if (!component) return;
		const parent = ss.getComponentById(component.parentId);
		if (!parent) return;
		const position = component.position;

		const siblings = ss.getComponents(parent.id);
		if (position == siblings.length - 1) return;

		const nextSibling = siblings.filter(
			(c) => c.position == position + 1
		)[0];

		const transactionId = `move-down-${componentId}`;
		ssbm.openMutationTransaction(transactionId, `Move down`);
		ssbm.registerPreMutation(nextSibling);
		nextSibling.position--;
		ssbm.registerPostMutation(nextSibling);
		ssbm.registerPreMutation(component);
		component.position++;
		ssbm.registerPostMutation(component);
		ssbm.closeMutationTransaction(transactionId);
		ss.sendComponentUpdate();
	}

	function moveComponent(
		componentId: Component["id"],
		newParentId: Component["id"],
		newPosition?: number
	) {
		const component = ss.getComponentById(componentId);
		if (!component) return;
		const currentParentComponent = ss.getComponentById(component.parentId);
		if (!currentParentComponent) return;
		if (componentId == newParentId) return;
		if (
			currentParentComponent.id == newParentId &&
			typeof newPosition == "undefined"
		)
			return;
		const transactionId = `move-${componentId}`;
		ssbm.openMutationTransaction(transactionId, `Move`);
		ssbm.registerPreMutation(component);
		repositionHigherSiblings(componentId, -1);
		component.position =
			newPosition ?? getNextInsertionPosition(newParentId);
		component.parentId = newParentId;
		repositionHigherSiblings(componentId, 1);
		ssbm.registerPostMutation(component);
		ssbm.closeMutationTransaction(transactionId);
		ss.sendComponentUpdate();
	}

	function createComponent(
		type: string,
		parentId: Component["id"],
		position?: number
	) {
		const newId = crypto.randomUUID();
		const definition = ss.getComponentDefinition(type);
		const { fields } = definition;
		const initContent = {};
		Object.entries(fields ?? {}).map(([fieldKey, field]) => {
			initContent[fieldKey] = field.init;
		});

		const component = {
			id: newId,
			type,
			parentId,
			content: initContent,
			handlers: {},
			position: position ?? getNextInsertionPosition(parentId),
			visible: true,
		};

		return component;
	}

	function createAndInsertComponent(
		type: string,
		parentId: Component["id"],
		position?: number
	) {
		const component = createComponent(type, parentId, position);
		const transactionId = `create-${component.id}`;
		ssbm.openMutationTransaction(transactionId, `Create`);
		ss.addComponent(component);
		repositionHigherSiblings(component.id, 1);
		ssbm.registerPostMutation(component);
		ssbm.closeMutationTransaction(transactionId);
		ss.sendComponentUpdate();
	}

	function repositionHigherSiblings(
		componentId: Component["id"],
		delta: number
	) {
		const component = ss.getComponentById(componentId);
		const siblings = ss
			.getComponents(component.parentId)
			.filter((c) => c.id !== componentId);
		const higherSiblings = siblings.filter(
			(siblingComponent) =>
				siblingComponent.position >= component.position
		);
		higherSiblings.map((c) => {
			ssbm.registerPreMutation(c);
			c.position += delta;
			ssbm.registerPostMutation(c);
		});
	}

	function getFlatComponentSubtree(
		componentId: Component["id"]
	): Component[] {
		const component = ss.getComponentById(componentId);
		const subtree: Component[] = [];

		const pushToSubtreeRecursively = (rootComponent: Component) => {
			const children = ss.getComponents(rootComponent.id);
			subtree.push(rootComponent);
			children.map((child) => pushToSubtreeRecursively(child));
		};

		pushToSubtreeRecursively(component);
		return subtree;
	}

	function removeComponentSubtree(componentId: Component["id"]): void {
		const component = ss.getComponentById(componentId);
		if (!component) return;
		const parentId = ss.getComponentById(componentId).parentId;

		const transactionId = `delete-${componentId}`;
		ssbm.openMutationTransaction(transactionId, `Delete`);
		if (parentId) {
			repositionHigherSiblings(component.id, -1);
		}
		const subtree = getFlatComponentSubtree(componentId);
		subtree.map((c) => ss.deleteComponent(c.id));

		subtree.map((c) => {
			ssbm.registerPreMutation(c);
			ss.deleteComponent(c.id);
		});
		ssbm.closeMutationTransaction(transactionId);
		ss.sendComponentUpdate();
	}

	function isParentViable(
		childType: string,
		parentId: Component["id"]
	): boolean {
		const containableTypes = ss.getContainableTypes(parentId);
		return containableTypes.includes(childType);
	}

	function isRoot(targetId: Component["id"]): boolean {
		return targetId == "root";
	}

	function isCopyAllowed(targetId: Component["id"]): boolean {
		return !isRoot(targetId);
	}

	function isCutAllowed(targetId: Component["id"]): boolean {
		return !isRoot(targetId);
	}

	function isDeleteAllowed(targetId: Component["id"]): boolean {
		return !isRoot(targetId);
	}

	function isGoToParentAllowed(targetId: Component["id"]): boolean {
		return !isRoot(targetId);
	}

	function goToParent(
		targetId: Component["id"],
		targetInstancePath?: string
	) {
		const targetComponent = ss.getComponentById(targetId);
		if (!targetComponent) return;
		const parentId = targetComponent.parentId;
		if (!parentId) return;

		let parentInstancePath: string;
		if (targetInstancePath) {
			parentInstancePath = targetInstancePath
				.split(",")
				.slice(0, -1)
				.join(",");
		}
		ssbm.setSelection(parentId, parentInstancePath);
	}

	function isPasteAllowed(targetId: Component["id"]): boolean {
		const clipboard = ssbm.getClipboard();
		if (clipboard === null) return false;
		const { jsonSubtree } = clipboard;
		const subtree = JSON.parse(jsonSubtree);
		if (subtree.length == 0) return false;
		const rootComponent = subtree[0];
		const { type: childType } = rootComponent;
		return isParentViable(childType, targetId);
	}

	function cutComponent(componentId: Component["id"]): void {
		const component = ss.getComponentById(componentId);
		if (!component) return;
		ssbm.setClipboard({
			operation: ClipboardOperation.Cut,
			jsonSubtree: JSON.stringify(getFlatComponentSubtree(componentId)),
		});
		ssbm.setSelection(null);
		removeComponentSubtree(componentId);
		ss.sendComponentUpdate();
	}

	function copyComponent(componentId: Component["id"]): void {
		const component = ss.getComponentById(componentId);
		if (!component) return;
		ssbm.setClipboard({
			operation: ClipboardOperation.Copy,
			jsonSubtree: JSON.stringify(getFlatComponentSubtree(componentId)),
		});
	}

	function pasteComponent(targetParentId: Component["id"]): void {
		const targetParent = ss.getComponentById(targetParentId);
		if (!targetParent) return;

		const clipboard = ssbm.getClipboard();
		if (clipboard === null) return;
		const { operation, jsonSubtree } = clipboard;
		const subtree = JSON.parse(jsonSubtree);
		if (operation == ClipboardOperation.Cut)
			return pasteCutComponent(targetParentId, subtree);
		if (operation == ClipboardOperation.Copy)
			return pasteCopyComponent(targetParentId, subtree);
	}

	function pasteCutComponent(
		targetParentId: Component["id"],
		subtree: Component[]
	) {
		// MUTATION

		ssbm.setClipboard(null);
		const rootComponent = subtree[0];
		rootComponent.parentId = targetParentId;
		rootComponent.position = getNextInsertionPosition(targetParentId);

		const transactionId = `paste-cut-${targetParentId}`;
		ssbm.openMutationTransaction(transactionId, `Paste from cut`);
		subtree.map((c) => {
			ss.addComponent(c);
			ssbm.registerPostMutation(c);
		});
		ssbm.closeMutationTransaction(transactionId);
		ss.sendComponentUpdate();
	}

	function pasteCopyComponent(
		targetParentId: Component["id"],
		subtree: Component[]
	) {
		// MUTATION

		const rootComponent = subtree[0];
		rootComponent.parentId = targetParentId;
		rootComponent.position = getNextInsertionPosition(targetParentId);

		subtree.forEach((c) => {
			const newId = crypto.randomUUID();
			subtree
				.filter((nc) => nc.id !== c.id)
				.map((nc) => {
					if (nc.parentId == c.id) {
						nc.parentId = newId;
					}
				});
			c.id = newId;
		});

		const transactionId = `paste-copy-${targetParentId}`;
		ssbm.openMutationTransaction(transactionId, `Paste from copy`);
		subtree.map((c) => {
			ss.addComponent(c);
			ssbm.registerPostMutation(c);
		});
		ssbm.closeMutationTransaction(transactionId);
		ss.sendComponentUpdate();
	}

	function getNextInsertionPosition(targetParentId: Component["id"]) {
		const children = ss.getComponents(targetParentId);

		if (children.length > 0) {
			const position =
				Math.max(...children.map((c: Component) => c.position)) + 1;
			return position;
		} else {
			return 0;
		}
	}

	function getUndoRedoSnapshot() {
		const snapshot = ssbm.getMutationTransactionsSnapshot();
		return {
			isUndoAvailable: !!snapshot.undo,
			isRedoAvailable: !!snapshot.redo,
			undoDesc: snapshot.undo?.desc,
			redoDesc: snapshot.redo?.desc,
		};
	}

	function undo() {
		const transaction = ssbm.consumeUndoTransaction();
		if (!transaction) return;

		Object.entries(transaction.mutations).forEach(
			([mutationId, mutation]) => {
				const component = ss.getComponentById(mutationId);

				if (mutation.jsonPre && mutation.jsonPost) {
					Object.assign(component, JSON.parse(mutation.jsonPre));
					return;
				}

				if (!mutation.jsonPre && mutation.jsonPost) {
					ss.deleteComponent(mutationId);
					return;
				}

				if (mutation.jsonPre && !mutation.jsonPost) {
					ss.addComponent(JSON.parse(mutation.jsonPre));
					return;
				}
			}
		);
		ss.sendComponentUpdate();
	}

	function redo() {
		const transaction = ssbm.consumeRedoTransaction();
		if (!transaction) return;

		Object.entries(transaction.mutations).forEach(
			([mutationId, mutation]) => {
				const component = ss.getComponentById(mutationId);

				if (mutation.jsonPre && mutation.jsonPost) {
					Object.assign(component, JSON.parse(mutation.jsonPost));
					return;
				}

				if (!mutation.jsonPre && mutation.jsonPost) {
					ss.addComponent(JSON.parse(mutation.jsonPost));
					return;
				}

				if (mutation.jsonPre && !mutation.jsonPost) {
					ss.deleteComponent(mutationId);
					return;
				}
			}
		);
		ss.sendComponentUpdate();
	}

	function setContentValue(
		componentId: Component["id"],
		fieldKey: string,
		value: string
	) {
		const component = ss.getComponentById(componentId);
		if (!component) return;
		const transactionId = `edit-${componentId}-content-${fieldKey}`;
		ssbm.openMutationTransaction(transactionId, `Edit property`, true);
		ssbm.registerPreMutation(component);

		component.content[fieldKey] = value;

		ssbm.registerPostMutation(component);
		ssbm.closeMutationTransaction(transactionId);
		ss.sendComponentUpdate();
	}

	function setVisibleValue(
		componentId: Component["id"],
		visible: Component["visible"]
	) {
		const component = ss.getComponentById(componentId);
		if (!component) return;
		const transactionId = `change-visibility-${componentId}`;
		ssbm.openMutationTransaction(transactionId, `Change visibility`, true);
		ssbm.registerPreMutation(component);
		component.visible = visible;
		ssbm.registerPostMutation(component);
		ssbm.closeMutationTransaction(transactionId);
		ss.sendComponentUpdate();
	}

	function setHandlerValue(
		componentId: Component["id"],
		eventType: string,
		userFunction: string
	) {
		const component = ss.getComponentById(componentId);
		if (!component) return;
		const transactionId = `set-handler-${componentId}`;
		ssbm.openMutationTransaction(transactionId, `Set event handler`, true);
		ssbm.registerPreMutation(component);

		if (userFunction) {
			component.handlers[eventType] = userFunction;
		} else {
			delete component.handlers[eventType];
		}

		ssbm.registerPostMutation(component);
		ssbm.closeMutationTransaction(transactionId);
		ss.sendComponentUpdate();
	}

	return {
		moveComponent,
		moveComponentUp,
		moveComponentDown,
		cutComponent,
		copyComponent,
		pasteComponent,
		createAndInsertComponent,
		removeComponentSubtree,
		isParentViable,
		isPasteAllowed,
		undo,
		redo,
		setContentValue,
		setVisibleValue,
		getUndoRedoSnapshot,
		setHandlerValue,
		isCopyAllowed,
		isCutAllowed,
		isDeleteAllowed,
		isGoToParentAllowed,
		goToParent,
	};
}
