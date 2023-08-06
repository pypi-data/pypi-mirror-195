const regex = /[\\]?@{([\w\s.]*)}/g;

export function parse(expr: string) {
	const result = [];
	const groups = [...expr.matchAll(regex)];

	for (let i = 0; i < groups.length; i++) {}

	const evaluatedExpr = expr.replace(regex, (match, captured) => {
		if (match.charAt(0) == "\\") return match.substring(1); // Escaped @, don't evaluate, return without \
		const trimmedCapture = captured.trim();
	});
}
