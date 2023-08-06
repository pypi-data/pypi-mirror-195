<template>
	<div class="CoreRoot" :style="rootStyle" data-streamsync-container>
		<template v-for="vnode in getChildrenVNodes()">
			<component
				:is="vnode"
				v-if="vnode.key === `${activePageId}:0`"
			></component>
		</template>
	</div>
</template>

<script lang="ts">
import { FieldCategory, FieldType } from "../streamsyncTypes";

export default {
	streamsync: {
		name: "Root",
		category: "Root",
		description: "Root component",
		allowedChildrenTypes: ["page"],
		fields: {
			appName: {
				name: "App name",
				type: FieldType.Text,
				desc: "The app name will be shown in the browser's title bar.",
			},
			accentColor: {
				name: "Accent",
				type: FieldType.Color,
				category: FieldCategory.Style,
			},
			primaryTextColor: {
				name: "Primary text",
				type: FieldType.Color,
				category: FieldCategory.Style,
			},
			secondaryTextColor: {
				name: "Secondary text",
				type: FieldType.Color,
				category: FieldCategory.Style,
			},
			emptinessColor: {
				name: "Emptiness",
				type: FieldType.Color,
				category: FieldCategory.Style,
			},
			containerBackgroundColor: {
				name: "Container background",
				type: FieldType.Color,
				category: FieldCategory.Style,
			},
			separatorColor: {
				name: "Separator",
				type: FieldType.Color,
				category: FieldCategory.Style,
			},
			buttonColor: {
				name: "Button",
				type: FieldType.Color,
				category: FieldCategory.Style,
			},
			buttonTextColor: {
				name: "Button text",
				type: FieldType.Color,
				category: FieldCategory.Style,
			},
		},
	},
};
</script>
<script setup lang="ts">
import { computed, inject } from "vue";
import injectionKeys from "../injectionKeys";

const ss = inject(injectionKeys.core);
const fields = inject(injectionKeys.evaluatedFields);
const getChildrenVNodes = inject(injectionKeys.getChildrenVNodes);

const rootStyle = computed(() => {
	return {
		"--accentColor": fields.value.accentColor,
		"--emptinessColor": fields.value.emptinessColor,
		"--containerBackgroundColor": fields.value.containerBackgroundColor,
		"--primaryTextColor": fields.value.primaryTextColor,
		"--secondaryTextColor": fields.value.secondaryTextColor,
		"--separatorColor": fields.value.separatorColor,
		"--buttonColor": fields.value.buttonColor,
		"--buttonTextColor": fields.value.buttonTextColor,
	};
});

const getFirstPageId = () => {
	const pageComponents = ss.getComponents("root", true);
	if (pageComponents.length == 0) return null;
	return pageComponents[0].id;
};

const activePageId = computed(() => {
	return ss.getActivePageId() ?? getFirstPageId();
});
</script>

<style scoped>
@import "../renderer/sharedStyles.css";

.CoreRoot {
	background: var(--emptinessColor);
	min-height: 100%;
	display: flex;
	width: 100%;
}

.CoreRoot.component.selected {
	background: var(--emptinessColor);
}
</style>
