<template>
	<div class="CorePage" :style="rootStyle">
		<div
			class="main"
			:class="{
				compact: fields.pageMode == 'compact',
				wide: fields.pageMode == 'wide',
			}"
			data-streamsync-container
		>
			<slot></slot>
		</div>
	</div>
</template>

<script lang="ts">
import { FieldCategory, FieldType } from "../streamsyncTypes";

export default {
	streamsync: {
		name: "Page",
		category: "Layout",
		description: "Page component",
		allowedChildrenTypes: ["*"],
		allowedParentTypes: ["root"],
		fields: {
			key: {
				name: "Page key",
				desc: "Unique identifier. Allows for the active page to be changed by calling state.set_active_page(key).",
				type: FieldType.Text,
			},
			pageMode: {
				name: "Page mode",
				init: "compact",
				type: FieldType.Text,
				control: "select",
				options: {
					compact: "Compact",
					wide: "Wide",
				},
				category: FieldCategory.Style,
			},
		},
		previewField: "key",
	},
};
</script>
<script setup lang="ts">
import { computed, inject } from "vue";
import injectionKeys from "../injectionKeys";

const fields = inject(injectionKeys.evaluatedFields);

const rootStyle = computed(() => {
	return {
		"--accentColor": fields.value.accentColor,
		"--emptinessColor": fields.value.emptinessColor,
		"--containerBackgroundColor": fields.value.containerBackgroundColor,
		"--primaryTextColor": fields.value.primaryTextColor,
		"--secondaryTextColor": fields.value.secondaryTextColor,
		"--separatorColor": fields.value.separatorColor,
	};
});
</script>

<style scoped>
@import "../renderer/sharedStyles.css";

.CorePage {
	width: 100%;
	min-height: 100%;
	background: var(--emptinessColor);
	display: flex;
	flex: 1 0 auto;
}

.main {
	min-height: 100%;
	overflow: hidden;
	padding: 24px;
}

.childless .main {
	background: var(--emptinessColor) !important;
}
.childless .main::after {
	content: "Empty Page. Drag and drop components from the Toolkit to get started." !important;
}
.main.compact {
	width: 100%;
	max-width: 1200px;
	margin-left: auto;
	margin-right: auto;
}
.main.wide {
	width: 100%;
}
</style>
