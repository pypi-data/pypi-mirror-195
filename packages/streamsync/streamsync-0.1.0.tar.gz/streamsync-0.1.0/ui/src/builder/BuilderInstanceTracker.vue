<template>
	<div class="BuilderInstanceTracker" :style="rootStyle" ref="rootEl">
		<slot></slot>
	</div>
</template>
<script setup lang="ts">
import { nextTick, onMounted, onUnmounted, Ref, ref, toRefs } from "vue";

const REFRESH_INTERVAL_MS = 200;

interface Props {
	instancePath: string;
	matchSize?: boolean;
	verticalOffsetPixels?: number;
}
const props = defineProps<Props>();
const { instancePath, matchSize, verticalOffsetPixels } = toRefs(props);

type RootStyle = {
	top: string;
	left: string;
	width: string;
	height: string;
};

const rootStyle: Ref<RootStyle> = ref(null);
const timerId = ref(0);
const rootEl: Ref<HTMLElement> = ref(null);
const rendererEl = document.querySelector(".ComponentRenderer");

const trackElement = (el: HTMLElement) => {
	const { offsetTop: top, offsetLeft: left } = el;
	const { clientWidth: rendererWidth, clientHeight: rendererHeight } =
		rendererEl;
	let { clientHeight: contentsHeight, clientWidth: contentsWidth } =
		matchSize?.value ? el : rootEl.value;

	let yAdjustment = verticalOffsetPixels?.value
		? verticalOffsetPixels.value
		: 0;

	const trackerTop = Math.min(
		Math.max(0, top + yAdjustment),
		rendererHeight - contentsHeight
	);
	const trackerLeft = Math.min(
		Math.max(0, left),
		rendererWidth - contentsWidth
	);

	// console.log(el, trackerTop, trackerLeft, top, left);

	// TODO only apply if coordinates actually changed

	rootStyle.value = {
		top: `${trackerTop}px`,
		left: `${trackerLeft}px`,
		width: `${contentsWidth}px`,
		height: `${contentsHeight}px`,
	};
};

const triggerTrack = () => {
	let el: HTMLElement = document.querySelector(
		`.ComponentRenderer [data-streamsync-instance-path="${instancePath.value}"]`
	);
	scheduleNextTrigger();
	if (!el) return;
	const elStyle = getComputedStyle(el);
	if (!elStyle) return;
	if (elStyle.display == "contents") {
		el = el.querySelector("[data-streamsync-id]");
	}
	if (!el) return;
	trackElement(el);
};

const scheduleNextTrigger = () => {
	timerId.value = setTimeout(triggerTrack, REFRESH_INTERVAL_MS);
};

onMounted(async () => {
	await nextTick();
	triggerTrack();
});

onUnmounted(() => {
	clearTimeout(timerId.value);
});
</script>

<style scoped>
.BuilderInstanceTracker {
	position: absolute;
	transition: all 0.2s ease-in-out;
	/* margin-top: -48px; */
	pointer-events: none;
}
</style>
