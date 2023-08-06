<template>
	<div
		class="BuilderComponentShortcuts"
		v-if="shortcutsInfo"
		:data-streamsync-id="componentId"
	>
		<div class="type">
			{{ shortcutsInfo?.componentTypeName }}
		</div>
		<template v-if="!isAddMode">
			<div
				class="actionButton"
				title="Add child"
				:class="{
					enabled: shortcutsInfo?.addEnabled,
				}"
				v-on:click="
					shortcutsInfo?.addEnabled
						? (isAddMode = !isAddMode)
						: undefined
				"
			>
				<i class="ri-add-line"></i>
			</div>
			<div
				class="actionButton"
				title="Move up (Ctrl+↑)"
				:class="{
					enabled: shortcutsInfo?.moveUpEnabled,
				}"
				v-on:click="
					shortcutsInfo?.moveUpEnabled
						? moveComponentUp(componentId)
						: undefined
				"
			>
				<i class="ri-arrow-up-line"></i>
			</div>
			<div
				class="actionButton"
				title="Move down (Ctrl+↓)"
				:class="{
					enabled: shortcutsInfo?.moveDownEnabled,
				}"
				v-on:click="
					shortcutsInfo?.moveDownEnabled
						? moveComponentDown(componentId)
						: undefined
				"
			>
				<i class="ri-arrow-down-line"></i>
			</div>

			<div
				class="actionButton"
				title="Cut (Ctrl+X)"
				:class="{
					enabled: shortcutsInfo?.cutEnabled,
				}"
				v-on:click="
					shortcutsInfo?.cutEnabled
						? cutComponent(componentId)
						: undefined
				"
			>
				<i class="ri-scissors-line"></i>
			</div>
			<div
				class="actionButton"
				title="Copy (Ctrl+C)"
				:class="{
					enabled: shortcutsInfo?.copyEnabled,
				}"
				v-on:click="
					shortcutsInfo?.copyEnabled
						? copyComponent(componentId)
						: undefined
				"
			>
				<i class="ri-file-copy-line"></i>
			</div>
			<div
				class="actionButton"
				title="Paste (Ctrl+V)"
				:class="{
					enabled: shortcutsInfo?.pasteEnabled,
				}"
				v-on:click="
					shortcutsInfo?.pasteEnabled
						? pasteComponent(componentId)
						: undefined
				"
			>
				<i class="ri-clipboard-line"></i>
			</div>
			<div
				class="actionButton"
				title="Go to parent (Ctrl+Shift+↑)"
				:class="{
					enabled: shortcutsInfo?.goToParentEnabled,
				}"
				v-on:click="
					shortcutsInfo?.goToParentEnabled
						? goToParent(componentId, instancePath)
						: undefined
				"
			>
				<i class="ri-parent-line"></i>
			</div>
			<div
				class="actionButton delete"
				title="Delete (Del)"
				:class="{
					enabled: shortcutsInfo?.deleteEnabled,
				}"
				v-on:click="
					shortcutsInfo?.deleteEnabled
						? removeComponentSubtree(componentId)
						: undefined
				"
			>
				<i class="ri-delete-bin-line"></i>
			</div>
		</template>
		<template v-if="isAddMode">
			<div class="addDialog">
				<input
					type="text"
					list="validChildrenTypes"
					placeholder="Component..."
					v-on:change="addComponent"
				/>
				<datalist id="validChildrenTypes">
					<option
						v-for="(definition, type) in validChildrenTypes"
						:value="definition.name"
					>
						{{ definition.name }}
					</option>
				</datalist>
			</div>
		</template>
	</div>
</template>

<script setup lang="ts">
import { computed, inject, onMounted, Ref, ref, toRefs, watch } from "vue";
import { useComponentActions } from "./useComponentActions";
import { Component, StreamsyncComponentDefinition } from "../streamsyncTypes";
import injectionKeys from "../injectionKeys";

const ss = inject(injectionKeys.core);
const ssbm = inject(injectionKeys.builderManager);

const {
	createAndInsertComponent,
	moveComponentUp,
	moveComponentDown,
	cutComponent,
	pasteComponent,
	copyComponent,
	isCopyAllowed,
	isCutAllowed,
	isGoToParentAllowed,
	isPasteAllowed,
	isDeleteAllowed,
	removeComponentSubtree,
	goToParent,
} = useComponentActions(ss, ssbm);

const props = defineProps<{
	componentId: Component["id"];
	instancePath: string;
}>();

const { componentId, instancePath } = toRefs(props);

const isAddMode = ref(false);

const shortcutsInfo: Ref<{
	componentTypeName: string;
	addEnabled: boolean;
	moveUpEnabled: boolean;
	moveDownEnabled: boolean;
	copyEnabled: boolean;
	cutEnabled: boolean;
	pasteEnabled: boolean;
	goToParentEnabled: boolean;
	deleteEnabled: boolean;
}> = ref(null);

const validChildrenTypes = computed(() => {
	const types = ss.getContainableTypes(componentId.value);
	const result: Record<string, StreamsyncComponentDefinition> = {};

	types.map((type) => {
		const definition = ss.getComponentDefinition(type);
		result[type] = definition;
	});

	return result;
});

function addComponent(event: Event) {
	const definitionName = (event.target as HTMLInputElement).value;
	const matchingTypes = Object.entries(validChildrenTypes.value).filter(
		([type, definition]) => {
			if (definition.name == definitionName) return true;
			return false;
		}
	);
	if (matchingTypes.length == 0) return;
	const type = matchingTypes[0][0];
	isAddMode.value = false;
	createAndInsertComponent(type, componentId.value);
}

function reprocessShorcutsInfo(): void {
	const component = ss.getComponentById(componentId.value);
	if (!component) return;
	const siblingCount = component.parentId
		? ss.getComponents(component.parentId).length
		: 0;
	shortcutsInfo.value = {
		addEnabled: ss.getContainableTypes(componentId.value).length > 0,
		componentTypeName: ss.getComponentDefinition(component.type)?.name,
		moveUpEnabled: siblingCount > 0 && component.position > 0,
		moveDownEnabled:
			siblingCount > 0 && component.position < siblingCount - 1,
		copyEnabled: isCopyAllowed(componentId.value),
		cutEnabled: isCutAllowed(componentId.value),
		pasteEnabled: isPasteAllowed(componentId.value),
		goToParentEnabled: isGoToParentAllowed(componentId.value),
		deleteEnabled: isDeleteAllowed(componentId.value),
	};
}

watch(
	() => ss.getComponentById(componentId.value)?.position,
	async (newPosition) => {
		if (typeof newPosition == "undefined" || newPosition === null) return;
		reprocessShorcutsInfo();
	},
	{ flush: "post" }
);

onMounted(() => {
	reprocessShorcutsInfo();
});
</script>

<style scoped>
@import "./sharedStyles.css";
.BuilderComponentShortcuts {
	display: flex;
	border-radius: 18px;
	box-shadow: 0 0 8px -1px rgba(0, 0, 0, 0.6);
	background: var(--builderBackgroundColor);
	pointer-events: auto;
	overflow: hidden;
}

.type {
	display: flex;
	align-items: center;
	padding-left: 16px;
	padding-right: 16px;
	height: 36px;
	background: var(--builderSelectedColor);
	cursor: grab;
}

.actionButton {
	width: 36px;
	height: 36px;
	display: flex;
	align-items: center;
	justify-content: center;
	color: var(--builderDisabledColor);
}

.actionButton:last-of-type {
	padding-right: 4px;
}

.actionButton.enabled {
	cursor: pointer;
	color: var(--builderPrimaryTextColor);
}

.actionButton.enabled.delete {
	color: var(--builderErrorColor);
}

.addDialog {
	display: flex;
	align-items: center;
	flex: 1 0 120px;
}

.addDialog input {
	flex: 1 0 auto;
	padding: 8px;
	height: 100%;
	outline: none;
	border: none;
}
</style>
