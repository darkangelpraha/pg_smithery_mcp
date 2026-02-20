# PostgreSQL MCP Server for Supabase

Model Context Protocol (MCP) server pro připojení k PostgreSQL databázi, zejména Supabase `pg_core_memory` databázi.

## Co projekt dělá

Tento MCP server poskytuje read-only přístup k PostgreSQL databázím přes Model Context Protocol. Umožňuje LLM modelům:
- Prohlížet databázové schéma (tabulky, sloupce, datové typy)
- Spouštět read-only SQL dotazy
- Získávat metadata o databázové struktuře

## Připojení k Supabase pg_core_memory

Pro připojení k Supabase databázi `pg_core_memory` použijte connection string ve formátu:

```
postgresql://[user]:[password]@[host]:[port]/pg_core_memory?sslmode=require
```

### Získání connection stringu z Supabase

1. Otevřete Supabase Dashboard
2. Přejděte na **Settings** → **Database**
3. V sekci **Connection string** zkopírujte **URI** nebo **Connection pooling** string
4. Nahraďte `[YOUR-PASSWORD]` skutečným heslem databáze
5. Ujistěte se, že databáze se jmenuje `pg_core_memory` (nebo upravte název v connection stringu)

### Příklad connection stringu

```
postgresql://postgres:[YOUR-PASSWORD]@db.xxxxxxxxxxxxx.supabase.co:5432/pg_core_memory?sslmode=require
```

## Instalace a použití

### Jako npm balíček

```bash
npm install -g @modelcontextprotocol/server-postgres
```

### Spuštění serveru

```bash
npx @modelcontextprotocol/server-postgres "postgresql://user:password@host:5432/pg_core_memory?sslmode=require"
```

### Konfigurace v Claude Desktop

Přidejte do `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "supabase-pg-core-memory": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-postgres",
        "postgresql://postgres:[YOUR-PASSWORD]@db.xxxxxxxxxxxxx.supabase.co:5432/pg_core_memory?sslmode=require"
      ]
    }
  }
}
```

**Poznámka:** Pro produkční použití použijte environment variables místo hardcodovaného hesla.

## Dostupné nástroje

- **query** - Spuštění read-only SQL dotazu na databázi
- **schema resources** - Prohlížení schématu tabulek v databázi

## Bezpečnost

- Server podporuje pouze **read-only** operace
- Všechny dotazy jsou spouštěny v transakcích s `READ ONLY` mode
- Pro write operace použijte jiný MCP server nebo přímé API

## Reference

Tento server je založen na oficiálním [Model Context Protocol PostgreSQL serveru](https://github.com/modelcontextprotocol/servers/tree/main/src/postgres).
