export function getDisciplineColor(discipline = "") {
  const d = discipline.toLowerCase();
  if (
    d.includes("electrical") ||
    d.includes("civil") ||
    d.includes("mechanical") ||
    d.includes("mechatronics") ||
    d.includes("machines")
  ) {
    return "var(--teal)";
  }
  if (
    d.includes("computer") ||
    d.includes("software") ||
    d.includes("artificial") ||
    d.includes("cloud") ||
    d.includes("architecture")
  ) {
    return "var(--violet-soft)";
  }
  if (
    d.includes("biomedical") ||
    d.includes("medical") ||
    d.includes("life") ||
    d.includes("generalised (medical)")
  ) {
    return "var(--coral)";
  }
  if (
    d.includes("aerospace") ||
    d.includes("astrophysics") ||
    d.includes("science") ||
    d.includes("generalised (science)")
  ) {
    return "var(--sky)";
  }
  return "var(--amber)";
}

export function getCatalogNumber(topicId = "", index = 0) {
  const parts = topicId.split("-");
  const code = parts.map((p) => p[0].toUpperCase()).join("").slice(0, 3);
  const num = String(index + 1).padStart(2, "0");
  return `${code}-${num}`;
}
