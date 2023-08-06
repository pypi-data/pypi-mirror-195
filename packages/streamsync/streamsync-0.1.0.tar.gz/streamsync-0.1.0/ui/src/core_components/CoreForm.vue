<template>
	<div class="CoreForm" ref="rootEl">
		<div data-streamsync-container><slot></slot></div>
		<div class="buttons">
			<button v-on:click="submit">{{ fields.submitDesc }}</button>
		</div>
	</div>
</template>

<script lang="ts">
import { Component, FieldType } from "../streamsyncTypes";

export default {
	streamsync: {
		name: "Form",
		description: "A form.",
		category: "Input",
		allowedChildrenTypes: ["*"],
		fields: {
			submitDesc: {
				name: "Submit Button Description",
				default: "(No description)",
				init: "Submit",
				type: FieldType.Text,
			},
		},
		events: {
			"ss-submit": {
				desc: "Submit the form.",
			},
		},
	},
};
</script>

<script setup lang="ts">
import { inject, ref, Ref } from "vue";
import injectionKeys from "../injectionKeys";

const fields = inject(injectionKeys.evaluatedFields);
const ss = inject(injectionKeys.core);
const componentId = inject(injectionKeys.componentId);
const rootEl: Ref<HTMLElement> = ref(null);

const getProcessedChildrenFormValues = async (parentId: Component["id"]) => {
	const processedFormValues = {};
	const childrenComponents = ss.getComponents(parentId);

	for (let i = 0; i < childrenComponents.length; i++) {
		const child = childrenComponents[i];
		const processedChildFormValues = await getProcessedChildrenFormValues(
			child.id
		);
		Object.assign(processedFormValues, processedChildFormValues);

		const formValue = ss.getFormValue(child.id);
		if (typeof formValue == "undefined") continue;
		let processedFormValue: any;
		if (typeof formValue == "function") {
			processedFormValue = await formValue();
		} else {
			processedFormValue = formValue;
		}

		const key = child.content.key ?? child.id;
		processedFormValues[key] = processedFormValue;
	}
	return processedFormValues;
};

const submit = async () => {
	const processedFormValues = await getProcessedChildrenFormValues(
		componentId
	);
	const event = new CustomEvent("ss-submit", {
		detail: { payload: processedFormValues },
	});
	rootEl.value.dispatchEvent(event);
};
</script>

<style scoped>
@import "../renderer/sharedStyles.css";

.buttons {
	margin-top: 16px;
}
</style>
