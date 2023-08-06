<template>
	<div class="CoreDataframe" :style="rootStyle">
		<table v-if="!isEmpty">
			<tr class="headerRow">
				<th></th>
				<th v-for="columnIndex in columnIndexes" :key="columnIndex">
					{{ columnIndex }}
				</th>
			</tr>
			<tr v-for="rowIndex in rowIndexes" :key="rowIndex">
				<td class="rowIndex">{{ rowIndex }}</td>
				<td v-for="columnName in columnIndexes" :key="columnName">
					{{ fields.dataframe[columnName][rowIndex] }}
				</td>
			</tr>
		</table>
		<div class="empty" v-else>Empty dataframe.</div>
	</div>
</template>

<script lang="ts">
import { computed, inject } from "vue";
import { FieldCategory, FieldType } from "../streamsyncTypes";

const defaultDataframe = `{
  "Column A": [1, 2, 3],
  "Column B": [4, 5, 6]
}`;

export default {
	streamsync: {
		name: "Dataframe",
		description: "Displays and allows interactions with dataframes.",
		category: "Content",
		fields: {
			dataframe: {
				name: "Data",
				desc: "Must be a JSON object or a state reference to a Pandas dataframe.",
				type: FieldType.Object,
				default: defaultDataframe,
			},
			primaryTextColor: {
				name: "Primary text",
				type: FieldType.Color,
				category: FieldCategory.Style,
			},
			secondaryTextColor: {
				name: "Secondary text",
				type: FieldType.Color,
				category: FieldCategory.Style,
			},
			backgroundColor: {
				name: "Background",
				type: FieldType.Color,
				category: FieldCategory.Style,
			},
			headerRowBackgroundColor: {
				name: "Header row background",
				type: FieldType.Color,
				category: FieldCategory.Style,
			},
			separatorColor: {
				name: "Separator",
				type: FieldType.Color,
				category: FieldCategory.Style,
			},
		},
	},
};
</script>
<script setup lang="ts">
import injectionKeys from "../injectionKeys";

const fields = inject(injectionKeys.evaluatedFields);

const columnIndexes = computed(() => {
	return Object.keys(fields.value.dataframe ?? {});
});
const isEmpty = computed(() => {
	const e = !fields.value.dataframe || columnIndexes.value.length == 0;
	return e;
});

const rowIndexes = computed(() => {
	const firstColumn = fields.value.dataframe[columnIndexes.value[0]];
	const rowIndexes = Object.keys(firstColumn);
	return rowIndexes;
});

const rootStyle = computed(() => {
	const style = {
		"--primaryTextColor": fields.value.primaryTextColor,
		"--secondaryTextColor": fields.value.secondaryTextColor,
		"--separatorColor": fields.value.separatorColor,
		"--CoreDataframe-backgroundColor": fields.value.backgroundColor,
		"--CoreDataframe-headerRowBackgroundColor": fields.value.headerRowBackgroundColor ?? "var(--separatorColor)",
	};
	return style;
});

</script>

<style scoped>
@import "../renderer/sharedStyles.css";

.CoreDataframe {
	background: var(--CoreDataframe-backgroundColor);
	font-size: 0.8rem;
	width: fit-content;
	max-width: 100%;
	max-height: 80vh;
	overflow: auto;
}

table {
	border-spacing: 0;
	border-collapse: collapse;
}

tr.headerRow > * {
	background-color: var(--CoreDataframe-headerRowBackgroundColor);
}

td,
th {
	border: 1px solid var(--separatorColor);
	padding: 8px;
	color: var(--primaryTextColor);
	font-weight: normal;
}

td.rowIndex {
	color: var(--secondaryTextColor);
}

</style>
