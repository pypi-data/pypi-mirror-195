<template>
	<div ref="rootEl">Timer</div>
</template>

<script lang="ts">
export default {
	streamsync: {
		name: "Timer",
		description: "Emits an event repeatedly, according to a time interval.",
		category: "Other",
	},
	fields: {
		intervalMillis: {
			name: "Interval (ms)",
			desc: "The ss-tick event will be fired repeatedly. This field allows you to configure the gap between the end of a call to the beginning of the next one.",
			init: "200",
			default: "200",
			type: FieldType.Number,
		},
	},
};
</script>

<script setup lang="ts">
import { inject, onMounted, Ref, ref } from "vue";
import { FieldType } from "../streamsyncTypes";

import injectionKeys from "../injectionKeys";
const fields = inject(injectionKeys.evaluatedFields);
const rootEl: Ref<HTMLElement> = ref(null);

const fireTimer = () => {
	setTimeout(() => {
		const event = new Event("tick");
		rootEl.value.dispatchEvent(event);
		fireTimer();
	}, fields.value.intervalMillis);
};
onMounted(() => {
	fireTimer();
});
</script>
