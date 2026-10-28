import "./ModelViewer.css";

export default function ModelViewer({ modelUrl, parts, onPartSelect, selectedPartId }) {
    function handleModelClick(event) {
        const modelViewer = event.target;
        const rect = modelViewer.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        const hit = modelViewer.positionAndNormalFromPoint(x, y);
        if (hit) {
            console.log(
                `position: "${hit.position.x.toFixed(3)}m ${hit.position.y.toFixed(3)}m ${hit.position.z.toFixed(3)}m"`
            );
        }
    }
    return (
        <model-viewer
            src={modelUrl}
            camera-controls
            auto-rotate
            shadow-intensity="1"
            style={{ width: "100%", height: "500px" }}
            onClick={handleModelClick}
        >
            {parts.map((part) => (
                <button
                    key={part.id}
                    slot={`hotspot-${part.id}`}
                    data-position={part.hotspotPosition}
                    data-normal="0m 1m 0m"
                    className={`hotspot ${selectedPartId === part.id ? "active" : ""}`}
                    onClick={() => onPartSelect(part.id)}
                >
                    {part.name}
                </button>
            ))}
        </model-viewer>
    );
}