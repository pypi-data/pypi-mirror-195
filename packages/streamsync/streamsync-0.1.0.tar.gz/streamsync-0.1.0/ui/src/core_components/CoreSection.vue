<template>
	<div class="CoreSection" :style="rootStyle">
		<h2 v-if="fields.title || fields.title == 0">{{ fields.title }}</h2>
		<div data-streamsync-container><slot></slot></div>
	</div>
</template>

<script lang="ts">
import { FieldCategory, FieldType } from "../streamsyncTypes";

const description = `Standard container with an optional title.`;

const docs = `
Like Streamlit, but fast. A proof-of-concept framework built using JavaScript/Vue.js + Python/Flask + WebSockets.

By avoiding a rerun of the whole script, Streamsync can react more than 70 times faster. This is all achieved while 
maintaining a similar syntax. This repository is a companion to the following Medium article (no paywall),
which explains how Streamsync was built, the tests conducted and the implications.
`;

export default {
	streamsync: {
		name: "Section",
		description,
		docs,
		category: "Layout",
		allowedChildrenTypes: ["*"],
		fields: {
			title: {
				name: "Title",
				init: "Section Title",
				desc: "Leave blank to hide.",
				type: FieldType.Text,
			},
			primaryTextColor: {
				name: "Primary text",
				type: FieldType.Color,
				category: FieldCategory.Style,
			},
			containerBackgroundColor: {
				name: "Container background",
				type: FieldType.Color,
				category: FieldCategory.Style,
			},
			containerShadow: {
				name: "Container shadow",
				type: FieldType.Shadow,
				category: FieldCategory.Style,
			},
			separatorColor: {
				name: "Separator",
				type: FieldType.Color,
				category: FieldCategory.Style,
			},
			secondaryTextColor: {
				name: "Secondary text",
				type: FieldType.Color,
				category: FieldCategory.Style,
			},
			accentColor: {
				name: "Accent",
				type: FieldType.Color,
				category: FieldCategory.Style,
			},
			emptinessColor: {
				name: "Emptiness",
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
		previewField: "title",
	},
};
</script>
<script setup lang="ts">
import { computed, inject } from "vue";
import injectionKeys from "../injectionKeys";

const fields = inject(injectionKeys.evaluatedFields);
const rootStyle = computed(() => {
	const style = {
		"--primaryTextColor": fields.value.primaryTextColor,
		"--containerBackgroundColor": fields.value.containerBackgroundColor,
		"--containerShadow": fields.value.containerShadow,
		"--separatorColor": fields.value.separatorColor,
		"--secondaryTextColor": fields.value.secondaryTextColor,
		"--accentColor": fields.value.accentColor,
		"--emptinessColor": fields.value.emptinessColor,
		"--buttonColor": fields.value.buttonColor,
		"--buttonTextColor": fields.value.buttonTextColor,
	};
	return style;
});
</script>

<style scoped>
@import "../renderer/sharedStyles.css";
.CoreSection {
	padding: 16px;
	border: 1px solid var(--separatorColor);
	border-radius: 8px;
	background-color: var(--containerBackgroundColor);
	box-shadow: var(--containerShadow);
}

h2 {
	margin-bottom: 16px;
}
</style>
