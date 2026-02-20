# Convert Structurizr JSON to Draw.io XML

Tento projekt obsahuje nástroje pro konverzi Structurizr JSON formátu do Draw.io XML formátu.

## Soubory

- `pg_icepanel_c4.json` - Původní Structurizr JSON soubor (zachován)
- `pg_icepanel_c4.drawio` - Vygenerovaný Draw.io XML soubor
- `convert_to_drawio.py` - Python skript pro konverzi
- `n8n_workflow_structurizr_to_drawio.json` - n8n workflow pro automatizaci

## Použití Python skriptu

```bash
python3 convert_to_drawio.py pg_icepanel_c4.json [output.drawio]
```

Pokud nezadáte výstupní soubor, vytvoří se automaticky `pg_icepanel_c4.drawio`.

## Použití n8n workflow

1. Importujte `n8n_workflow_structurizr_to_drawio.json` do n8n
2. Upravte cestu k vstupnímu souboru v node "Read JSON File"
3. Spusťte workflow
4. Výstupní `.drawio` soubor bude vytvořen

## Otevření v Draw.io

1. Otevřete [app.diagrams.net](https://app.diagrams.net)
2. File > Open from > Device
3. Vyberte `pg_icepanel_c4.drawio`
4. Diagram se načte s C4 elementy

## Formát Draw.io XML

Draw.io používá XML formát založený na mxGraph knihovně:
- `<mxfile>` - root element
- `<diagram>` - jednotlivý diagram
- `<mxGraphModel>` - grafický model
- `<mxCell>` - jednotlivé elementy (shapes, connectors)

## C4 Model elementy

- **People** (Aktéři) - zelená/modrá barva podle location
- **Software Systems** - zelená (Internal) / žlutá (External)
- **Containers** - modrá barva
- **Components** - oranžová barva
- **Relationships** - šedé čáry s popisky

## Poznámky

- Původní JSON soubor zůstává nezměněn
- Draw.io soubor lze editovat přímo v app.diagrams.net
- Pro lepší layout použijte Draw.io automatické rozložení (Arrange > Layout)
