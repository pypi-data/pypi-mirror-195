<template>
	<div class="CoreDateInput" ref="rootEl">
		<div class="main">
			<div class="inputContainer">
				<label>{{ fields.label }}</label>
				<input type="date" v-model="inputValue" />
			</div>
		</div>
	</div>
</template>

<script lang="ts">
import { FieldType } from "../streamsyncTypes";

export default {
	streamsync: {
		name: "Date Input",
		description: "Allows the user to enter a date.",
		category: "Input",
		fields: {
			label: {
				name: "Label",
				init: "Input Label",
				type: FieldType.Text,
			},
			key: {
				name: "Key",
				type: FieldType.Text,
			},
			initialValue: {
				name: "Initial value",
				type: FieldType.Text,
				default: "",
			},
		},
		events: {
			"ss-change": {
				desc: "Capture changes to this control.",
			},
		},
	},
};
</script>
<script setup lang="ts">
import { inject, onMounted, Ref, ref, watch } from "vue";
import injectionKeys from "../injectionKeys";

const fields = inject(injectionKeys.evaluatedFields);
const setFormValue = inject(injectionKeys.setFormValue);
const rootEl: Ref<HTMLElement> = ref(null);

const inputValue = ref(fields.value.initialValue);

onMounted(() => {
	setFormValue(inputValue.value);
});

watch(inputValue, (newValue: string) => {
	const event = new CustomEvent("ss-change", {
		detail: { payload: newValue },
	});
	rootEl.value.dispatchEvent(event);
	setFormValue(newValue);
});
</script>

<style scoped>
@import "../renderer/sharedStyles.css";

.CoreDateInput {
	width: fit-content;
}

label {
	display: block;
	margin-bottom: 8px;
}

input {
	max-width: 20ch;
	width: 100%;
	margin: 0;
	border: 1px solid var(--separatorColor);
}
</style>
