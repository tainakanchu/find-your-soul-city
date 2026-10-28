import { knowledge } from "../data.ts";

interface Props {
  /** cityId -> total score (0–100). Omitted: plain dots. */
  scores?: Map<string, number>;
  /** City id to mark as #1. */
  pin?: string;
  label: string;
}

const x = (lon: number) => lon + 180;
const y = (lat: number) => 90 - lat;

/** Equirectangular plot of every city in the dataset. No basemap: only the graticule. */
export function WorldPlot({ scores, pin, label }: Props) {
  const pinned = knowledge.cities.find((c) => c.id === pin);
  return (
    <svg className="world" viewBox="0 0 360 160" role="img" aria-label={label}>
      <g className="graticule">
        {[-150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150].map((lon) => (
          <line key={lon} x1={x(lon)} x2={x(lon)} y1={y(70)} y2={y(-70)} />
        ))}
        {[-60, -30, 30, 60].map((lat) => (
          <line key={lat} x1={0} x2={360} y1={y(lat)} y2={y(lat)} />
        ))}
        <line className="equator" x1={0} x2={360} y1={y(0)} y2={y(0)} />
      </g>
      {knowledge.cities.map((c) => {
        const s = scores?.get(c.id);
        const r = s === undefined ? 1.6 : 1 + (s / 100) * 3.4;
        return (
          <circle
            key={c.id}
            className={s === undefined ? "dot" : "dot scored"}
            cx={x(c.lon)}
            cy={y(c.lat)}
            r={r}
            style={s === undefined ? undefined : { opacity: 0.25 + (s / 100) * 0.75 }}
          >
            <title>{s === undefined ? c.nameJa : `${c.nameJa} ${Math.round(s)}`}</title>
          </circle>
        );
      })}
      {pinned && <circle className="pin" cx={x(pinned.lon)} cy={y(pinned.lat)} r={5.5} />}
    </svg>
  );
}
