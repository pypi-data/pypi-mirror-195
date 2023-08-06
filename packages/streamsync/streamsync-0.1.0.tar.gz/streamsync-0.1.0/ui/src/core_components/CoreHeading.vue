<template>
	<div class="CoreHeading" :style="{ 'text-align': fields.alignment }">
		<h1>{{ fields.text }}</h1>
	</div>
</template>

<script lang="ts">
export default {
	streamsync: {
		name: "Heading",
		description: "Provides a text heading (title).",
		category: "Content",
		fields: {
			text: {
				name: "Text",
				default: "(No text)",
				init: "Heading Text",
				type: FieldType.Text,
			},
			alignment: {
				name: "Alignment",
				default: null,
				init: "left",
				type: FieldType.Text,
				control: "select",
				options: {
					left: "Left",
					center: "Center",
					right: "Right",
				},
			},
		},
		previewField: "text",
	},
};
</script>
<script setup lang="ts">
import { inject } from "vue";
import { FieldType } from "../streamsyncTypes";
import injectionKeys from "../injectionKeys";
const fields = inject(injectionKeys.evaluatedFields);
</script>
<style scoped>
@import "../renderer/sharedStyles.css";
</style>
