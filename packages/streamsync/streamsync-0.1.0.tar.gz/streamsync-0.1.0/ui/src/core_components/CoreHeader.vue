<template>
	<div class="CoreHeader" :style="rootStyle">
		<div class="rectangle">
			<h1>{{ fields.text }}</h1>
		</div>
	</div>
</template>

<script lang="ts">
export default {
	streamsync: {
		name: "Header",
		description: "Serves as top-level component.",
		category: "Layout",
		fields: {
			text: {
				name: "Text",
				init: "Header Text",
				default: "(No text)",
				type: FieldType.Text,
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
		"--accentColor": fields.value.accentColor,
		"--emptinessColor": fields.value.emptinessColor,
	};
	return style;
});

</script>

<style scoped>
@import "../renderer/sharedStyles.css";

.rectangle {
	background: var(--accentColor);
	padding: 16px;
	width: fit-content;
}

h1 {
	color: var(--emptinessColor);
}
</style>
