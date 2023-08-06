<template>
	<div :style="rootStyle">
		<button class="CoreButton">
			{{ fields.text }}
		</button>
	</div>
</template>

<script lang="ts">
const clickHandlerStub = `
def handle_button_click(state):

	# Increment counter when the button is clicked

	state["counter"] += 1`;

export default {
	streamsync: {
		name: "Button",
		description:
			"A standalone button, which can be linked to a click event.",
		category: "Input",
		events: {
			click: {
				desc: "Capture single clicks.",
				stub: clickHandlerStub.trim(),
			},
		},
		fields: {
			text: {
				name: "Text",
				init: "Button Text",
				type: FieldType.Text,
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
			buttonShadow: {
				name: "Button shadow",
				type: FieldType.Shadow,
				category: FieldCategory.Style,
			},
			separatorColor: {
				name: "Separator",
				type: FieldType.Color,
				category: FieldCategory.Style,
			},
		},
		previewField: "text",
	},
};
</script>
<script setup lang="ts">
import { computed, inject } from "vue";
import { FieldCategory, FieldType } from "../streamsyncTypes";
import injectionKeys from "../injectionKeys";

const fields = inject(injectionKeys.evaluatedFields);

const rootStyle = computed(() => {
	const style = {
		"--buttonColor": fields.value.buttonColor,
		"--buttonTextColor": fields.value.buttonTextColor,
		"--separatorColor": fields.value.separatorColor,
		"--buttonShadow": fields.value.buttonShadow,
	};
	return style;
});

</script>

<style scoped>
@import "../renderer/sharedStyles.css";

</style>
