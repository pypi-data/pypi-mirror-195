<template>
	<div class="CoreRadioInput" ref="rootEl">
		<div class="main">
			<div class="inputContainer">
				<label class="mainLabel">{{ fields.label }}</label>
				<div class="options">
					<div
						class="option"
						v-for="(option, optionKey) in fields.options"
						:key="optionKey"
					>
						<input
							type="radio"
							v-model="inputValue"
							:value="optionKey"
							:id="`${flattenedInstancePath}-option-${optionKey}`"
							:name="`${flattenedInstancePath}-options`"
						/><label
							:for="`${flattenedInstancePath}-option-${optionKey}`"
							>{{ option }}</label
						>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script lang="ts">
import { computed, inject, onMounted, Ref, watch } from "vue";
import { ref } from "vue";
import { FieldType } from "../streamsyncTypes";

const defaultOptions = { a: "Option A", b: "Option B" };

const onChangeHandlerStub = `
def onchange_handler(state, payload):

	# Set the state variable "selected" to the selected radio option

	state["selected"] = payload`;

export default {
	streamsync: {
		name: "Radio Input",
		description: "Allows the user to choose a value using radio buttons.",
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
			options: {
				name: "Options",
				control: "object",
				desc: "Key-value object with options. Must be a JSON string or a state reference to a dictionary.",
				type: FieldType.KeyValue,
				default: JSON.stringify(defaultOptions, null, 2),
			},
		},
		events: {
			"ss-option-change": {
				desc: "Sent when the selected option changes.",
				stub: onChangeHandlerStub.trim(),
			},
		},
	},
};
</script>

<script setup lang="ts">
import injectionKeys from "../injectionKeys";
const setFormValue = inject(injectionKeys.setFormValue);
const fields = inject(injectionKeys.evaluatedFields);
const componentId = inject(injectionKeys.componentId);
const instancePath = inject(injectionKeys.instancePath);
const rootEl: Ref<HTMLElement> = ref(null);
const inputValue = ref(null);
onMounted(() => {
	setFormValue(inputValue.value);
});

watch(inputValue, (newValue) => {
	const event = new CustomEvent("ss-option-change", {
		detail: { payload: newValue },
	});
	rootEl.value.dispatchEvent(event);
	setFormValue(newValue);
});

const flattenedInstancePath = computed(() => {
	const flat = instancePath
		.map((item) => `${item.componentId}:${item.instanceNumber}`)
		.join(".");
	return flat;
});
</script>

<style scoped>
@import "../renderer/sharedStyles.css";
.CoreRadioInput {
	width: 100%;
}

.options {
	display: flex;
	flex-direction: column;
	margin-top: 4px;
}

.option {
	margin-top: 8px;
	display: flex;
	align-items: center;
	color: var(--primaryTextColor);
}

input {
	margin: 0 8px 0 0;
}

label {
	color: var(--primaryTextColor);
}
</style>
