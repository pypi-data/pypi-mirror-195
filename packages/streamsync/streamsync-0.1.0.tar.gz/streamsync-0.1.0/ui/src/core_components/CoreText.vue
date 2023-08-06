<template>
	<div class="CoreText" :style="{ 'text-align': fields.alignment }">
		<template v-if="fields.useMarkdown == 'no'">
			<div class="plainText">{{ fields.text }}</div>
		</template>
		<template v-else-if="fields.useMarkdown == 'yes'">
			<div
				class="markdown"
				v-dompurify-html="unsanitisedMarkdownHtml"
			></div>
		</template>
	</div>
</template>

<script lang="ts">
import { FieldType } from "../streamsyncTypes";

export default {
	streamsync: {
		name: "Text",
		description: "Displays plain or Markdown text.",
		category: "Content",
		fields: {
			text: {
				name: "Text",
				default: "(No text)",
				init: "Text",
				type: FieldType.Text,
				control: "textarea",
			},
			useMarkdown: {
				name: "Use Markdown",
				desc: "The Markdown output will be sanitised; unsafe elements will be removed.",
				init: "no",
				type: FieldType.Text,
				control: "select",
				options: {
					yes: "Yes",
					no: "No",
				},
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
import { marked } from "marked";
import { computed, inject } from "vue";
import injectionKeys from "../injectionKeys";
const fields = inject(injectionKeys.evaluatedFields);

const unsanitisedMarkdownHtml = computed(() => {
	const unsanitisedHtml = marked.parse(fields.value.text);
	return unsanitisedHtml;
});
</script>

<style scoped>
@import "../renderer/sharedStyles.css";

.CoreText {
	color: var(--primaryTextColor);
}

.plainText {
	white-space: pre-wrap;
}
</style>
