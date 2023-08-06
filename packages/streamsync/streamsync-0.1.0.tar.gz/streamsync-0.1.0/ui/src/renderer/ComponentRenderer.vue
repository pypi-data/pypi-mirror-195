<template>
	<div class="ComponentRenderer" tabindex="-1" :style="rootStyle">
		<RendererNotifications class="notifications"></RendererNotifications>
		<div class="rootComponentArea">
			<ComponentProxy
				v-if="rootComponent"
				:component-id="rootComponent.id"
				:instance-path="rootInstancePath"
				:instance-data="rootInstanceData"
			></ComponentProxy>
			<slot></slot>
		</div>
	</div>
</template>

<script setup lang="ts">
import { inject, ref, Ref, computed, watch } from "vue";
import { Component, InstancePath } from "../streamsyncTypes";
import ComponentProxy from "./ComponentProxy.vue";
import RendererNotifications from "./RendererNotifications.vue";
import injectionKeys from "../injectionKeys";
import { useTemplateEvaluator } from "./useTemplateEvaluator";

const ss = inject(injectionKeys.core);
const templateEvaluator = useTemplateEvaluator(ss);
const pages: Component[] = ss.getComponents();
const thing = ref([]);

if (pages.length == 0) {
	console.error("No pages found.");
}

const rootInstancePath: InstancePath = [
	{ componentId: "root", instanceNumber: 0 },
];
const rootInstanceData = [ref(null)];
const rootComponent: Ref<Component> = ref(pages[0]);
const rootFields = computed(() =>
	templateEvaluator.getEvaluatedFields(rootInstancePath)
);
const rootStyle = computed(() => {
	return {
		"--accentColor": rootFields.value.accentColor,
		"--emptinessColor": rootFields.value.emptinessColor,
		"--containerBackgroundColor": rootFields.value.parentIdBackgroundColor,
		"--primaryTextColor": rootFields.value.primaryTextColor,
		"--secondaryTextColor": rootFields.value.secondaryTextColor,
		"--separatorColor": rootFields.value.separatorColor,
	};
});

watch(
	() => rootFields.value.appName,
	(appName: string) => {
		updateTitle(appName);
	},
	{ immediate: true }
);

function updateTitle(appName: string) {
	const mode = ss.getMode();
	let title: string;
	if (appName && mode == "edit") {
		title = `${appName} | Streamsync Builder`;
	} else if (!appName && mode == "edit") {
		title = "Streamsync Builder";
	} else if (appName && mode == "run") {
		title = `${appName}`;
	} else if (!appName && mode == "run") {
		title = "Streamsync App";
	}
	document.title = title;
}
</script>

<style scoped>
@import "./sharedStyles.css";

.ComponentRenderer {
	--accentColor: #29cf00;
	--buttonColor: #ffffff;
	--emptinessColor: #fafafa;
	--separatorColor: rgba(0, 0, 0, 0.07);
	--subtleHighlight: rgba(0, 0, 0, 0.03);
	--primaryTextColor: #3a3f40;
	--buttonTextColor: #3a3f40;
	--secondaryTextColor: #4f5e62;
	--containerBackgroundColor: #ffffff;
	width: 100%;
	outline: none;
	--notificationsDisplacement: 0;
	font-family: Inter, sans-serif;
	font-size: 0.8rem;
	color: var(--primaryTextColor);
	background: var(--emptinessColor);
	display: flex;
	flex-direction: column;
	min-height: 100%;
	isolation: isolate;
	flex: 1 0 auto;
}
.notifications {
	position: absolute;
	right: var(--notificationsDisplacement);
}

.rootComponentArea {
	display: flex;
	flex: 1 0 auto;
	position: relative;
}
</style>
