<template>
	<div class="CoreColumns horizontal" data-streamsync-container>
		<slot></slot>
	</div>
</template>

<script lang="ts">
export default {
	streamsync: {
		name: "Column Container",
		description: "Serves as container for Column components",
		allowedChildrenTypes: ["column", "repeater"],
		category: "Layout",
	},
};
</script>

<style scoped>
@import "../renderer/sharedStyles.css";

.CoreColumns {
	width: 100%;
	max-width: 100%;
	display: flex;
	flex-wrap: nowrap;
	flex-direction: row;
}
</style>
