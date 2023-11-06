# spanish-verb-conjugator-cli
Originally as a study aid for my Spanish 1 and Spanish 2 courses in High School.
The initial project simply parsed the JSON data containing the conjugations of
a given verb and dumped them into a text file.

Revisiting the project, I decided to pull it forward, utilizing the new
`@dataclass` available in Python 3.7.

In lieu of dumping the output into a text file, the output is now displayed
in the console in the form of a conjugation t-table popularly utilized in
Spanish courses that follows the following structure:

```
yo              | nosotros
tú              | vosotros
el/ella, usted  | ellos/ellas, ustededes
```

## Requirements
- `python >= 3.7+`
- `requests`
- `prettytable`

## Usage
`python3 main.py VERB`

### Example
``` bash
python3 main.py descargar

+--------------------------+
|       Participles        |
+------------+-------------+
|    Past    |   Present   |
+------------+-------------+
| descargado | descargando |
+------------+-------------+
+-------------------------+
|    Present Indicative   |
+-----------+-------------+
|  descargo | descargamos |
| descargas |  descargáis |
|  descarga |  descargan  |
+-----------+-------------+
+-----------------------------+
|     Preterite Indicative    |
+-------------+---------------+
|  descargué  |  descargamos  |
| descargaste | descargasteis |
|   descargó  |  descargaron  |
+-------------+---------------+
+-----------------------------+
|     Imperfect Indicative    |
+-------------+---------------+
|  descargaba | descargábamos |
| descargabas |  descargabais |
|  descargaba |  descargaban  |
+-------------+---------------+
+-------------------------------+
|     Conditional Indicative    |
+--------------+----------------+
| descargaría  | descargaríamos |
| descargarías | descargaríais  |
| descargaría  |  descargarían  |
+--------------+----------------+
```
