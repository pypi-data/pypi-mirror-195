import { Ref, ref } from "vue";
import { Core, Component } from "../streamsyncTypes";
import { CANDIDATE_CONFIRMATION_DELAY_MS } from "./builderManager";

/*
In Renderer, the drag and drop of components goes through two phases:

1. Unconfirmed candidate phase. 
Insertion overlay is updated as the user hovers over different component and
viable parents. These potential parents are "candidates".
After CANDIDATE_CONFIRMATION_DELAY_MS milliseconds, the active potential 
parent becomes a confirmed candidate.
If the drop happens before the candidate is confirmed, no position is provided.

2. Confirmed candidate phase.
When a candidate is confirmed, the user loses the ability to switch to another candidate.
The confirmed candidate's container is "cracked open" and its insertion slots are revealed.
The insertion slots will allow the user to choose an exact position in which
to insert the dragged component.

*/

const candidateId: Ref<Component["id"]> = ref(null);
const candidateInstancePath: Ref<string> = ref(null);
const isCandidacyConfirmed: Ref<boolean> = ref(false);
let candidacyStartTime: number = null;
let insertionPosition: number = null;

export function useDragDropComponent(ss: Core) {
	function getComponentInfoFromDrag(ev: DragEvent) {
		const parameter: string = ev.dataTransfer.types[0].split(";")[1];
		const [draggedType, draggedId] = parameter.split(",");
		return { draggedType, draggedId };
	}

	function getIdFromElement(el: HTMLElement) {
		// Elements inside a cage aren't taken into account for insertion

		const cageEl = el.closest("[data-streamsync-cage]");
		const startEl = cageEl ?? el;
		let targetEl: HTMLElement = startEl.closest("[data-streamsync-id]");
		if (!targetEl) return;
		return targetEl.dataset.streamsyncId;
	}

	function dropComponent(ev: DragEvent) {
		const dropTargetId = getIdFromElement(ev.target as HTMLElement);
		const { draggedType, draggedId } = getComponentInfoFromDrag(ev);
		const parentId = findSuitableParent(dropTargetId, draggedType);
		if (!parentId) return;
		const dropData = {
			draggedType,
			draggedId: draggedId,
			parentId: candidateId.value,
			position: insertionPosition,
		};
		removeInsertionCandidacy(ev);
		return dropData;
	}

	function findSuitableParent(
		targetId: Component["id"],
		insertedType: Component["type"]
	): Component["id"] {
		const targetComponent = ss.getComponentById(targetId);
		if (!targetComponent) return;
		const containableTypes = ss.getContainableTypes(targetId);

		if (containableTypes.includes(insertedType)) {
			return targetId;
		}

		if (!targetComponent.parentId) return null;
		return findSuitableParent(targetComponent.parentId, insertedType);
	}

	function assignInsertionCandidacy(ev: DragEvent) {
		if (isCandidacyConfirmed.value) {
			handleConfirmedCandidacy(ev);
			return;
		}

		handleUnconfirmedCandidacy(ev);
	}

	function handleUnconfirmedCandidacy(ev: DragEvent) {
		const { draggedType, draggedId } = getComponentInfoFromDrag(ev);
		const targetEl = ev.target as HTMLElement;
		const dropTargetId = getIdFromElement(targetEl);
		const parentId = findSuitableParent(dropTargetId, draggedType);
		if (!parentId || parentId == draggedId) return;
		const parentComponentEl: HTMLElement = targetEl.closest(
			`[data-streamsync-id="${parentId}"]`
		);
		const parentComponentInstancePath =
			parentComponentEl.dataset.streamsyncInstancePath;
		ev.preventDefault();

		if (candidateInstancePath.value !== parentComponentInstancePath) {
			candidacyStartTime = Date.now();
		} else if (
			Date.now() - candidacyStartTime >=
			CANDIDATE_CONFIRMATION_DELAY_MS
		) {
			isCandidacyConfirmed.value = true;
			crackContainerOpen(candidateInstancePath.value);
			return;
		}

		candidateId.value = parentId;
		candidateInstancePath.value = parentComponentInstancePath;
	}

	function handleConfirmedCandidacy(ev: DragEvent) {
		ev.preventDefault();

		const { draggedId } = getComponentInfoFromDrag(ev);
		const slotEls = getSlotElementsOfCrackedContainer(
			candidateInstancePath.value
		);
		if (slotEls.length == 0) return;
		const nearestSlotEl = getNearestSlot(ev.clientX, ev.clientY, slotEls);
		if (!nearestSlotEl) return;

		const slotPosition = parseInt(nearestSlotEl.dataset.streamsyncPosition);
		const draggedComponent = ss.getComponentById(draggedId);

		slotEls.map((el) => {
			if (!el.classList.contains("highlighted")) return;
			el.classList.remove("highlighted");
		});
		if (nearestSlotEl.classList.contains("highlighted")) return;
		nearestSlotEl.classList.add("highlighted");

		if (
			draggedComponent &&
			draggedComponent.parentId == candidateId.value &&
			slotPosition > draggedComponent.position
		) {
			// Account for the component staying in the same container.

			insertionPosition = slotPosition - 1;
			return;
		}

		insertionPosition = slotPosition;
	}

	function getSlotElementsOfCrackedContainer(instancePath: string) {
		const el = getContainerInInstancePath(instancePath);
		const slotEls: HTMLElement[] = Array.from(
			el.querySelectorAll(`[data-streamsync-position]`)
		);
		return slotEls;
	}

	function getNearestSlot(x: number, y: number, slotEls: HTMLElement[]) {
		// Calculate distance from nearest vertex and sort

		slotEls.sort((a, b): number => {
			const getDistance = (el: HTMLElement) => {
				const { top, left, right, bottom } = el.getBoundingClientRect();
				const dx = Math.max(left - x, 0, x - right);
				const dy = Math.max(top - y, 0, y - bottom);
				return Math.sqrt(dx * dx + dy * dy);
			};
			return getDistance(a) > getDistance(b) ? 1 : -1;
		});

		return slotEls[0];
	}

	/**
	 * Cracks a container open, revealing its insertion slots.
	 */
	function crackContainerOpen(instancePath: string) {
		const el = getContainerInInstancePath(instancePath);
		el.classList.add("crackedContainer");
	}

	function restoreCrackedContainer(instancePath: string) {
		const el = getContainerInInstancePath(instancePath);
		el.classList.remove("crackedContainer");
	}

	function getContainerInInstancePath(instancePath: string) {
		let el: HTMLElement = document.querySelector(
			`[data-streamsync-instance-path="${instancePath}"]`
		);
		if (!el.hasAttribute("data-streamsync-container")) {
			el = el.querySelector("[data-streamsync-container]");
		}
		return el;
	}

	function removeInsertionCandidacy(ev: Event): void {
		ev.preventDefault();
		if (candidateInstancePath.value) {
			restoreCrackedContainer(candidateInstancePath.value);
			candidateInstancePath.value = null;
		}
		candidateId.value = null;
		candidacyStartTime = null;
		insertionPosition = null;
		isCandidacyConfirmed.value = false;
	}

	return {
		candidateId,
		candidateInstancePath,
		isCandidacyConfirmed,
		getComponentInfoFromDrag,
		dropComponent,
		assignInsertionCandidacy,
		removeInsertionCandidacy,
	};
}
