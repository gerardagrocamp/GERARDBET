# GerardBet

Web de análisis de apuestas de fútbol para **LaLiga**, **Copa del Rey**, **Supercopa de España** y **Champions League** (temporada 2026-27).

Es una sola página (`index.html`) que funciona en cualquier navegador, sin servidor ni instalación.

## Qué hace

- **Calendario real por jornadas.** Abre en la jornada en juego, con horario peninsular español, y se puede pasar de jornada con las flechas, la tira de números o deslizando el dedo.
- **Análisis de cada partido.**
  - Probabilidades 1·X·2 y goles esperados.
  - Unos 25 mercados con su % de éxito: resultado, doble oportunidad, goles, ambos marcan, córners, tarjetas, tiros a puerta y apuestas de jugador.
- **Cuotas orientativas.**
  - **Cuota real:** el 1X2, tomado de OddsPortal.
  - **Cuota de mercado:** doble oportunidad, goles y ambos marcan, calculados a partir de ese 1X2.
  - **Est.:** el resto de mercados, con la cuota estimada por el modelo.
  - Puedes escribir tu propia cuota, elegir la casa de apuestas y ver si la apuesta tiene valor.
- **Cara a cara entre los dos equipos.**
  - Goles, rachas, córners, tiros, faltas, paradas y tarjetas.
  - Filtro para ver todos los partidos, solo los de casa o solo los de fuera.
- **Plantillas reales.**
  - LaLiga y los rivales de Champions, con selector de jugador.
  - Ficha de cada jugador con su % de éxito en el partido: marcar, tiros a puerta, faltas y paradas.
- **Modo creación de apuesta.**
  - Eliges los partidos de una jornada, el rango de cuota y el máximo de selecciones.
  - La web propone una combinada con las selecciones más probables, mezclando tipos de mercado.

## Cómo verla

**En tu ordenador:** descarga el repositorio y abre `index.html` con el navegador.

**Publicada con GitHub Pages:**
1. Sube el repositorio a GitHub.
2. Ve a **Settings → Pages**.
3. En *Source* elige **Deploy from a branch**, la rama `main` y la carpeta `/ (root)`.
4. Guarda. En uno o dos minutos la web estará en `https://TU-USUARIO.github.io/NOMBRE-DEL-REPOSITORIO/`.

## Estructura

```
index.html              La web lista para usar (generada)
scripts/
  template.html         Diseño y código de la página
  build.py              Une la plantilla con los datos y genera index.html
data/
  openfootball/*.json   Calendarios de las ligas (openfootball)
  results.txt           Resultados recientes de liga
  cups.txt              Champions, Copa del Rey y Supercopa
  odds.txt              Cuotas 1X2 de mercado
  squads_es.txt         Plantillas de LaLiga
  squads_ucl.txt        Plantillas de los rivales de Champions
  scorers_es.txt        Máximos goleadores de LaLiga
```

## Cómo actualizar los datos

1. Edita los ficheros de `data/`.
   - **Resultados:** `results.txt` usa el formato `liga|jornada|local|visitante|goles-goles`, y `cups.txt` usa `competición|ronda|fecha|hora|local|visitante|goles-goles`.
   - **Cuotas:** `odds.txt` usa el formato `competición|fecha|local|visitante|cuota1|cuotaX|cuota2`.
   - **Plantillas:** en `squads_*.txt`, cada equipo empieza con una línea `#Equipo`, seguida de un jugador por línea con el formato `Nombre,POS` (POS es POR, DEF, MED o DEL).
2. Regenera la página (necesitas Python 3):

   ```
   python3 scripts/build.py
   ```

3. Sube los cambios a GitHub.

## Cómo se calcula

- **Goles esperados.** Salen del ataque y la defensa de cada equipo, calculados con sus resultados reales de la temporada y una valoración previa de su nivel. Cuando hay cuota de mercado, se ajustan a ella: 70% mercado y 30% modelo.
- **Probabilidad de cada marcador.** Se obtiene con una distribución de Poisson. De ahí salen el 1X2, los goles y el ambos marcan.
- **Córners, tarjetas, tiros, faltas, paradas y estadísticas de jugador.** Son **estimaciones** según la posición y el rendimiento del equipo. No hay datos públicos completos de cada jugador para esta temporada.
- **Probabilidad de la combinada.** Es el producto de las probabilidades de cada selección, suponiendo que son independientes.

## Fuentes

- Calendarios: [openfootball/football.json](https://github.com/openfootball/football.json)
- Resultados: [futboltotal.futbol](https://futboltotal.futbol)
- Champions y plantillas inscritas: [UEFA.com](https://www.uefa.com/uefachampionsleague/)
- Plantillas de LaLiga: [Comuniate](https://www.comuniate.com)
- Goleadores: [Renderfoot](https://www.renderfoot.com/es/top-scorers/la-liga)
- Cuotas: [OddsPortal](https://www.oddsportal.com)

## Aviso

GerardBet es una herramienta orientativa. Las probabilidades son estimaciones de un modelo y no garantizan ningún resultado. Comprueba siempre la cuota en tu casa de apuestas antes de apostar.

**Juego responsable:** solo para mayores de 18 años. Si el juego deja de ser un entretenimiento, tienes ayuda en [jugarbien.es](https://www.jugarbien.es) o en el 900 200 225.
