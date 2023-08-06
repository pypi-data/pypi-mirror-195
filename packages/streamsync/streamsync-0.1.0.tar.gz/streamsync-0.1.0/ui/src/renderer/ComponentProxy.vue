<script lang="ts">
import { computed, h, inject, provide, ref } from "vue";
import templateMap from "../core/templateMap";
import { Component, InstancePath, InstancePathItem } from "../streamsyncTypes";
import ComponentProxy from "./ComponentProxy.vue";
import { useTemplateEvaluator } from "./useTemplateEvaluator";
import injectionKeys from "../injectionKeys";
import { VNode } from "vue";
import ChildlessPlaceholder from "./ChildlessPlaceholder.vue";

const fallbackRender = (type: string) =>
	h("div", `Component type ${type} not supported.`);

export default {
	props: ["componentId", "instancePath", "instanceData"],
	setup(props) {
		const ss = inject(injectionKeys.core);
		const ssbm = inject(injectionKeys.builderManager);
		const componentId: Component["id"] = props.componentId;
		const component = computed(() => ss.getComponentById(componentId));
		const template = templateMap[component.value.type];
		if (!template) return fallbackRender(component.value.type);
		const instancePath: InstancePath = props.instancePath;
		const instanceData = props.instanceData;
		const templateEvaluator = useTemplateEvaluator(ss);
		const evaluatedFields = computed(() =>
			templateEvaluator.getEvaluatedFields(instancePath)
		);

		const children = computed(() => ss.getComponents(componentId, true));

		const getChildlessPlaceholderVNode = (): VNode => {
			if (children.value.length > 0) return;
			if (component.value.type == "html") return;
			return h(ChildlessPlaceholder, {
				componentId: component.value.id,
			});
		};

		const renderProxiedComponent = (
			componentId: Component["id"],
			instanceNumber: InstancePathItem["instanceNumber"] = 0
		) => {
			const vnode = h(ComponentProxy, {
				componentId,
				key: `${componentId}:${instanceNumber}`,
				instancePath: [
					...instancePath,
					{
						componentId: componentId,
						instanceNumber,
					},
				],
				instanceData: [...instanceData, ref(null)],
			});
			return vnode;
		};

		const getChildrenVNodes = (
			instanceNumber: InstancePathItem["instanceNumber"] = 0
		): VNode[] => {
			const renderInsertionSlot = (position: number) => {
				return h("div", {
					"data-streamsync-slot-of-id": componentId,
					"data-streamsync-position": position,
				});
			};

			// Include slots if ssbm is present.

			const childrenVNodes = children.value.map(
				(childComponent, childIndex) => {
					const childVNode = renderProxiedComponent(
						childComponent.id,
						instanceNumber
					);
					return [
						childVNode,
						...(ssbm ? [renderInsertionSlot(childIndex + 1)] : []),
					];
				}
			);
			return [...(ssbm ? [renderInsertionSlot(0)] : [])].concat(
				childrenVNodes.flat()
			);
		};

		provide(injectionKeys.evaluatedFields, evaluatedFields);
		provide(injectionKeys.componentId, componentId);
		provide(injectionKeys.setFormValue, (v: string) =>
			ss.setFormValue(componentId, v)
		);
		provide(injectionKeys.instancePath, instancePath);
		provide(injectionKeys.instanceData, instanceData);
		provide(injectionKeys.renderProxiedComponent, renderProxiedComponent);
		provide(injectionKeys.getChildrenVNodes, getChildrenVNodes);

		const flattenInstancePath = (path: InstancePath) => {
			return path
				.map((ie) => `${ie.componentId}:${ie.instanceNumber}`)
				.join(",");
		};

		const dataAttrs = {
			"data-streamsync-id": componentId,
			"data-streamsync-instance-path": flattenInstancePath(instancePath),
		};

		const isChildless = computed(() => children.value.length == 0);
		const isSelected = computed(() => ssbm?.getSelectedId() == componentId);
		const isVisible = computed(() => ss.isComponentVisible(componentId));

		const getHandlerCallable = (handlerFunction: string) => {
			const isForwardable = !handlerFunction.startsWith("$");
			if (isForwardable) {
				return (ev: Event) => ss.forwardEvent(ev, instancePath);
			}
			if (handlerFunction.startsWith("$goToPage_")) {
				const pageKey = handlerFunction.substring("$goToPage_".length);
				return (ev: Event) => ss.setActivePageFromKey(pageKey);
			}
			return null;
		};

		const eventHandlerProps = computed(() => {
			const props = {};
			Object.entries(component.value.handlers).forEach(
				([handlerEventType, handlerFunction]) => {
					const eventBindingKey = `on${handlerEventType
						.charAt(0)
						.toUpperCase()}${handlerEventType.slice(1)}`;
					props[eventBindingKey] =
						getHandlerCallable(handlerFunction);
				}
			);
			return props;
		});

		const getRootElProps = function () {
			const rootElProps = {
				class: {
					component: true,
					childless: isChildless.value,
					selected: isSelected.value,
				},
				style: !isVisible.value ? { display: "none" } : {},
				...dataAttrs,
				...eventHandlerProps.value,
				draggable: !!ssbm,
			};
			return rootElProps;
		};

		return () => {
			const defaultSlotFn = isChildless.value
				? getChildlessPlaceholderVNode
				: ({ instanceNumber }: { instanceNumber: number }) =>
						getChildrenVNodes(instanceNumber);

			const vnodeProps = {
				...getRootElProps(),
			};
			const renderedComponent = h(template, vnodeProps, {
				default: defaultSlotFn,
			});

			return renderedComponent;
		};
	},
};
</script>
<style scoped>
@import "../renderer/sharedStyles.css";
</style>
