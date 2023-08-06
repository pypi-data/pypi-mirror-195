<template>
	<div class="CoreFileInput">
		<div class="main">
			<div class="inputContainer">
				<label>{{ fields.label }}</label>
				<input
					type="file"
					v-on:change="fileChange($event as InputEvent)"
					:multiple="allowMultipleFilesFlag"
				/>
			</div>
		</div>
	</div>
</template>

<script lang="ts">
import { FieldType } from "../streamsyncTypes";

export default {
	streamsync: {
		name: "File Input",
		description: "Upload files",
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
				desc: "Assigns a key to be used when processing a Form submission.",
			},
			allowMultipleFiles: {
				name: "Allow multiple files",
				init: "no",
				type: FieldType.Text,
				control: "select",
				options: {
					yes: "Yes",
					no: "No",
				},
			},
		},
	},
};
</script>

<script setup lang="ts">
import { computed, inject, onMounted } from "vue";
import injectionKeys from "../injectionKeys";
const setFormValue = inject(injectionKeys.setFormValue);
const fields = inject(injectionKeys.evaluatedFields);

onMounted(() => {
	setFormValue("");
});

const allowMultipleFilesFlag = computed(() => {
	return fields.value.allowMultipleFiles == "yes" ? true : undefined;
});

const encodeFile = async (file: File) => {
	var reader = new FileReader();
	reader.readAsDataURL(file);

	return new Promise((resolve, reject) => {
		reader.onload = () => resolve(reader.result);
		reader.onerror = () => reject(reader.error);
	});
};

const fileChange = (ev: InputEvent) => {
	const el = ev.target as HTMLInputElement;
	if (!el.files || el.files.length == 0) return;

	const value = async () => {
		const encodedFiles = await Promise.all(
			Array.from(el.files).map(async (f) => await encodeFile(f))
		);
		return encodedFiles;
	};

	setFormValue(value);
};
</script>

<style scoped>
@import "../renderer/sharedStyles.css";

.CoreFileInput {
	width: 100%;
}

label {
	display: block;
	margin-bottom: 8px;
}

input {
	max-width: 70ch;
	width: 100%;
	margin: 0;
	border: 1px solid var(--separatorColor);
}
</style>
