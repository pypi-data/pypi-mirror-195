<template>
	<template v-if="!templateField.control || templateField.control == 'text'">
		<input
			class="BuilderFieldsText"
			type="text"
			:value="component.content[fieldKey]"
			v-on:input="handleInput"
			autocorrect="off"
			autocomplete="off"
			spellcheck="false"
	/></template>
	<template v-else-if="templateField.control == 'textarea'">
		<textarea
			v-capture-tabs
			class="BuilderFieldsText"
			:value="component.content[fieldKey]"
			v-on:input="handleInput"
			:placeholder="templateField?.default"
			autocorrect="off"
			autocomplete="off"
			spellcheck="false"
		>
		</textarea>
	</template>
	<template v-else-if="templateField.control == 'select'">
		<select
			class="BuilderFieldsText"
			:value="component.content[fieldKey]"
			v-on:input="handleInput"
			autocorrect="off"
			autocomplete="off"
			spellcheck="false"
		>
			<option
				v-for="(option, optionKey) in templateField.options"
				:value="optionKey"
			>
				<template
					v-if="option.toLowerCase() !== optionKey.toLowerCase()"
				>
					{{ optionKey }} ({{ option }})
				</template>
				<template v-else>
					{{ optionKey }}
				</template>
			</option>
		</select>
	</template>
</template>

<script setup lang="ts">
import { toRefs, inject, computed } from "vue";
import { Component } from "../streamsyncTypes";
import { useComponentActions } from "./useComponentActions";
import injectionKeys from "../injectionKeys";

const ss = inject(injectionKeys.core);
const ssbm = inject(injectionKeys.builderManager);
const { setContentValue } = useComponentActions(ss, ssbm);

const props = defineProps<{
	componentId: Component["id"];
	fieldKey: string;
}>();
const { componentId, fieldKey } = toRefs(props);
const component = computed(() => ss.getComponentById(componentId.value));
const templateField = computed(() => {
	const { type } = component.value;
	const definition = ss.getComponentDefinition(type);
	return definition.fields[fieldKey.value];
});

const handleInput = (ev: Event) => {
	setContentValue(
		component.value.id,
		fieldKey.value,
		(ev.target as HTMLInputElement).value
	);
};
</script>

<style scoped>
@import "./sharedStyles.css";

.BuilderFieldsText {
	padding: 16px 12px 12px 12px;
	width: 100%;
}
</style>
