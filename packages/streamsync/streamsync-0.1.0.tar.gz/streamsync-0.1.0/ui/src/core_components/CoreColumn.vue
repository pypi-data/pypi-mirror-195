<template>
	<div
		class="CoreColumn"
		:style="{ flex: `${fields.width}` }"
		data-streamsync-container
	>
		<slot></slot>
	</div>
</template>

<script lang="ts">
import { FieldType } from "../streamsyncTypes";
export default {
	streamsync: {
		name: "Column",
		description:
			"Organises components in columns. Must have a Column Container parent.",
		allowedParentTypes: ["columns", "repeater"],
		allowedChildrenTypes: ["*"],
		category: "Layout",
		fields: {
			width: {
				name: "Width (basis)",
				default: "1",
				init: "1",
				type: FieldType.Text,
			},
		},
	},
};
</script>
<script setup lang="ts">
import { inject } from "vue";
import injectionKeys from "../injectionKeys";

const fields = inject(injectionKeys.evaluatedFields);
</script>

<style scoped>
@import "../renderer/sharedStyles.css";

.CoreColumn {
}
</style>
