import { Ref } from "vue";
import { ComponentMap } from ".";
import { Component } from "../streamsyncTypes";
import templateMap from "./templateMap";

function getParentAllowedSet(
	components: Ref<ComponentMap>,
	componentId: Component["id"]
): Set<string> {
	const parentId = components.value[componentId].parentId;
	if (!parentId) return new Set([]);
	return getAllowedSet(components, parentId);
}

function getDisallowedSet(
	components: Ref<ComponentMap>,
	componentId: Component["id"]
) {
	const { type } = components.value[componentId];
	const supportedTypes = Object.keys(templateMap);
	const typesAndDefs = supportedTypes.map((type) => ({
		type,
		definition: templateMap[type]?.streamsync,
	}));
	const disallowedDefs = typesAndDefs.filter(
		(tad) =>
			tad.definition.allowedParentTypes &&
			!tad.definition.allowedParentTypes.includes(type)
	);

	return new Set(disallowedDefs.map((tad) => tad.type));
}

function getAllowedSet(
	components: Ref<ComponentMap>,
	componentId: Component["id"]
) {
	const { type } = components.value[componentId];
	const supportedTypes = Object.keys(templateMap);
	const { allowedChildrenTypes } = templateMap[type].streamsync;
	if (!allowedChildrenTypes) return new Set([]);

	let allowed = new Set<string>(allowedChildrenTypes);
	if (allowedChildrenTypes.includes("*")) {
		return new Set(supportedTypes);
	}
	if (allowed.delete("inherit")) {
		const parentAllowed = getParentAllowedSet(components, componentId);
		allowed = new Set([...allowed, ...parentAllowed]);
	}
	return allowed;
}

export function getContainableTypes(
	components: Ref<ComponentMap>,
	componentId: Component["id"]
) {
	const allowed = Array.from(getAllowedSet(components, componentId));
	const disallowed = Array.from(getDisallowedSet(components, componentId));
	const containable = allowed.filter((type) => !disallowed.includes(type));

	return containable;
}
