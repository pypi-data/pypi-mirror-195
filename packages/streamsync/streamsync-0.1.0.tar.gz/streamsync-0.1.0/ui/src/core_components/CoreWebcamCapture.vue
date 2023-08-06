<template>
	<div class="CoreWebcamCapture" ref="rootEl">
		<div class="main">
			<video autoplay="true" ref="videoEl"></video>
		</div>
		<div class="actions">
			<button v-if="refreshRate == 0" v-on:click="sendFrame">
				Capture image
			</button>

			<button v-on:click="toggleActive">
				{{ isActive ? "Stop" : "Resume" }}
			</button>
			<select v-if="videoDevices?.length > 1" v-model="preferredDeviceId">
				<option
					v-for="device in videoDevices"
					:key="device.deviceId"
					:value="device.deviceId"
				>
					{{ device.label }}
				</option>
			</select>
		</div>
	</div>
</template>

<script lang="ts">
import { FieldType } from "../streamsyncTypes";

export default {
	streamsync: {
		name: "Webcam Capture",
		description: "Allows the user to take pictures using their webcam.",
		category: "Input",
		fields: {
			refreshRate: {
				name: "Refresh rate (ms)",
				init: "200",
				default: "200",
				desc: "Set to 0 for manual capture.",
				type: FieldType.Number,
			},
		},
		events: {
			"ss-webcam": {
				desc: "Sent when a frame is captured. Its payload contains the captured frame in PNG format.",
			},
		},
	},
};
</script>

<script setup lang="ts">
import {
	computed,
	inject,
	onBeforeUnmount,
	onMounted,
	Ref,
	ref,
	watch,
} from "vue";
import injectionKeys from "../injectionKeys";

const isActive = ref(true);
const rootEl: Ref<HTMLElement> = ref(null);
const canvasEl = document.createElement("canvas");
const videoEl: Ref<HTMLVideoElement> = ref(null);
const fields = inject(injectionKeys.evaluatedFields);
const videoDevices: Ref<MediaDeviceInfo[]> = ref(null);
const preferredDeviceId: Ref<MediaDeviceInfo["deviceId"]> = ref(null);

onMounted(async () => {
	videoDevices.value = await getVideoDevices();
	preferredDeviceId.value = videoDevices.value?.[0]?.deviceId;
	await startCapture();

	// Send first frame, which will start a chain of events if applicable.

	sendFrame();
});

onBeforeUnmount(() => {
	stopCapture();
});

const getVideoDevices = async () => {
	const devices = await navigator.mediaDevices.enumerateDevices();
	return devices.filter((d) => d.kind == "videoinput");
};

const refreshRate = computed(() => {
	return fields.value?.refreshRate;
});

watch(refreshRate, (newRate, prevRate) => {
	if (newRate > 0 && prevRate <= 0) {
		sendFrame();
	}
});

watch(preferredDeviceId, async () => {
	stopCapture();
	await startCapture();
});

const toggleActive = async () => {
	isActive.value = !isActive.value;
	if (!isActive.value) {
		stopCapture();
		return;
	}
	await startCapture();
	sendFrame();
};

const getFrameAsDataURL = () => {
	const context = canvasEl.getContext("2d");
	context.drawImage(videoEl.value, 0, 0);
	const dataURL = canvasEl.toDataURL("image/png");
	return dataURL;
};

const sendFrame = () => {
	const event = new CustomEvent("ss-webcam", {
		detail: {
			payload: getFrameAsDataURL(),
			callback: () => {
				if (refreshRate.value <= 0 || !isActive.value) return;
				setTimeout(() => {
					sendFrame();
				}, refreshRate.value);
			},
		},
	});

	rootEl.value.dispatchEvent(event);
};

const startCapture = async (): Promise<void> => {
	videoEl.value.style.display = null;

	return new Promise((resolve, reject) => {
		if (!navigator.mediaDevices.getUserMedia) {
			console.error("This browser doesn't support webcam connection.");
			reject();
		}

		const constraints: MediaStreamConstraints = { video: true };
		if (videoDevices.value.length > 1) {
			constraints.video = {
				deviceId: preferredDeviceId.value,
			};
		}

		navigator.mediaDevices
			.getUserMedia(constraints)
			.then((stream) => {
				videoEl.value.srcObject = stream;
				const webcamWidth = stream
					.getVideoTracks()[0]
					.getSettings().width;
				const webcamHeight = stream
					.getVideoTracks()[0]
					.getSettings().height;
				canvasEl.setAttribute("width", webcamWidth.toString());
				canvasEl.setAttribute("height", webcamHeight.toString());
				resolve();
			})
			.catch((error) => {
				console.error(
					"An error occurred when trying to use the webcam.",
					error
				);
				reject();
			});
	});
};

const stopCapture = () => {
	const stream = videoEl.value.srcObject as MediaStream;

	if (stream) {
		const tracks = stream.getTracks();
		tracks.map((track) => track.stop());
	}

	videoEl.value.srcObject = null;
	videoEl.value.style.display = "none";
};
</script>

<style scoped>
@import "../renderer/sharedStyles.css";

.CoreWebcamCapture {
	width: 100%;
}

video {
	width: 100%;
	max-width: 70ch;
}

.actions {
	margin-top: 16px;
	display: flex;
	gap: 16px;
}
</style>
