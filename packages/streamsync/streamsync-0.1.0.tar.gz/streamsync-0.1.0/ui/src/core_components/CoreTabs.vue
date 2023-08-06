<template>
	<div class="CoreTabs" :style="rootStyle">
		<div
			class="tabSelector horizontal"
			data-streamsync-cage
			data-streamsync-container
		>
			<slot :instance-number="0"></slot>
		</div>
		<div class="container">
			<slot :instance-number="1"></slot>
		</div>
	</div>
</template>

<script lang="ts">
export default {
	streamsync: {
		name: "Tab Container",
		description: "Displays Tab components.",
		category: "Layout",
		allowedChildrenTypes: ["tab", "repeater"],
		fields: {
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
		},
	},
};
</script>
<script setup lang="ts">
import { computed, inject } from "vue";
import injectionKeys from "../injectionKeys";
import { FieldCategory, FieldType } from "../streamsyncTypes";

const fields = inject(injectionKeys.evaluatedFields);
const instanceData = inject(injectionKeys.instanceData);
instanceData.at(-1).value = { activeTab: undefined };

const rootStyle = computed(() => {
	const style = {
		"--accentColor": fields.value.accentColor,
		"--primaryTextColor": fields.value.primaryTextColor,
		"--secondaryTextColor": fields.value.secondaryTextColor,
		"--containerBackgroundColor": fields.value.containerBackgroundColor,
		"--separatorColor": fields.value.separatorColor,
	};
	return style;
});
</script>

<style scoped>
@import "../renderer/sharedStyles.css";

.CoreTabs {
	width: 100%;
}

.CoreTabs.selected {
	background: transparent !important;
}

.tabSelector {
	pointer-events: all;
	border-radius: 8px 8px 0 0;
	background: var(--containerBackgroundColor);
	overflow: hidden;
	display: flex;
	gap: 16px;
	width: fit-content;
	border-top: 1px solid var(--separatorColor);
	border-left: 1px solid var(--separatorColor);
	border-right: 1px solid var(--separatorColor);
	color: var(--secondaryTextColor);
	padding: 0 16px 0 16px;
}

.childless > .tabSelector {
	display: none;
}

.container {
	border: 1px solid var(--separatorColor);
	background: var(--containerBackgroundColor);
	border-radius: 0 8px 8px 8px;
	overflow: hidden;
}

.childless > .container {
	border-radius: 8px;
}
</style>
