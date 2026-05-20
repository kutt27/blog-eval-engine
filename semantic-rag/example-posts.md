# example-posts.md

**Purpose:** Provides few-shot exemplars of well-structured blog posts across different types. The evaluation engine can reference these to compare the submitted content against established structural patterns.

---

## 1. Tutorial (How-to)

### Exemplar Structure
```markdown
# How to Set Up PostgreSQL with Node.js in 10 Minutes

**Meta:** A concise, step-by-step tutorial that takes a beginner from zero to a working PostgreSQL connection in Node.js.

## Prerequisites
- Node.js v18+ installed
- PostgreSQL 14+ installed and running
- Basic JavaScript knowledge

## What You'll Build
A simple REST API that reads and writes user data to a PostgreSQL database.

## Step 1: Initialize the Project
```bash
mkdir node-pg-demo && cd node-pg-demo
npm init -y
npm install express pg dotenv
```

## Step 2: Configure the Database Connection
Create a `.env` file:
```
DATABASE_URL=postgresql://localhost:5432/mydb
```

Create `db.js`:
```javascript
const { Pool } = require('pg');
const pool = new Pool({ connectionString: process.env.DATABASE_URL });
module.exports = pool;
```

## Step 3: Create the Database Table
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
```

## Step 4: Build the API Routes
```javascript
const express = require('express');
const pool = require('./db');
const app = express();
app.use(express.json());

app.get('/users', async (req, res) => {
  const result = await pool.query('SELECT * FROM users');
  res.json(result.rows);
});

app.post('/users', async (req, res) => {
  const { name, email } = req.body;
  const result = await pool.query(
    'INSERT INTO users (name, email) VALUES ($1, $2) RETURNING *',
    [name, email]
  );
  res.status(201).json(result.rows[0]);
});

app.listen(3000, () => console.log('Server running on port 3000'));
```

## Step 5: Verify It Works
```bash
# Terminal 1: Start the server
node index.js

# Terminal 2: Test the API
curl http://localhost:3000/users
curl -X POST http://localhost:3000/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice","email":"alice@example.com"}'
```

## Troubleshooting
- **ECONNREFUSED:** Make sure PostgreSQL is running (`pg_isready`)
- **password authentication failed:** Check your `pg_hba.conf` settings
- **relation does not exist:** Run the CREATE TABLE command first
```

### What Makes This Exemplary
- **Prerequisites block** before step 1 ✓
- **Expected outcome** stated upfront ✓
- **Atomic steps** — each step is a single action ✓
- **Verification step** to confirm success ✓
- **Troubleshooting section** for common errors ✓
- **Runnable code** with imports included ✓

---

## 2. Comparison (X vs Y)

### Exemplar Structure
```markdown
# Prisma vs. Drizzle ORM: Choosing the Right Tool for Your Stack

**Meta:** An unbiased technical comparison of two popular TypeScript ORMs, with a decision framework.

## Why These Two?
Prisma and Drizzle are the two most popular TypeScript ORMs in 2024, but they take fundamentally different approaches to database interaction.

## Feature Matrix

| Feature | Prisma | Drizzle |
|---------|--------|---------|
| Query syntax | Declarative (Prisma Schema) | SQL-like (TypeScript) |
| Bundle size | ~15 MB | ~800 KB |
| Migration files | Auto-generated | Hand-written SQL |
| Edge support | Via @prisma/adapter-* | First-class |
| Learning curve | Medium | Steep (requires SQL) |
| Type safety | Excellent | Excellent |

## Choose Prisma If...
- You're building a monolith with complex relations
- You want auto-generated migrations
- Your team prefers declarative schemas
- You're using PostgreSQL or MySQL

## Choose Drizzle If...
- You're building serverless or edge functions
- Bundle size matters (e.g., Lambda cold starts)
- Your team is comfortable writing raw SQL
- You need SQLite support

## The Nuance
Prisma's query engine adds ~15 MB to your deploy size, which matters for serverless. Drizzle has no runtime overhead but requires more SQL knowledge. Both produce equivalent SQL at the database level.
```

### What Makes This Exemplary
- **Context** explaining why these two are compared ✓
- **Feature matrix** with parallel columns ✓
- **"Choose X if..."** sections with specific criteria ✓
- **Nuance section** acknowledging trade-offs ✓
- **No false equivalence** — clear decision framework ✓

---

## 3. Opinion / Editorial

### Exemplar Structure
```markdown
# Why I Stopped Using TypeScript Enums (And You Should Too)

**Meta:** A strong, evidence-backed opinion challenging a common TypeScript practice.

**Thesis:** TypeScript enums create more problems than they solve. Const objects with union types are superior in every modern codebase.

## Pillar 1: Enums Are Not Tree-Shakeable
When bundling with Webpack or esbuild, enums produce IIFE code that cannot be tree-shaken...

## Pillar 2: Numeric Enums Are Unsafe
```typescript
enum Status { Active, Inactive }
const s: Status = 999; // No error! Numeric enums allow any number
```

## Pillar 3: String Enums Are Verbose
```typescript
// Instead of:
enum Color { Red = "red", Green = "green" }

// Use:
const Color = { Red: "red", Green: "green" } as const;
type Color = (typeof Color)[keyof typeof Color];
```

## The Counterargument (Steel Man)
"Yes, enums provide runtime value-to-name mapping that const objects don't."

**Response:** You almost never need this in practice. When you do, `Object.entries()` on a const object works identically.

## Conclusion
Migrate your enums to const objects. Your bundle size will shrink, your types will be safer, and you'll remove a footgun from your codebase.
```

### What Makes This Exemplary
- **Clear thesis** in first 10% ✓
- **3-5 supporting pillars** with evidence ✓
- **"Steel Man" counterargument** ✓
- **Conclusive stance** with action item ✓
- **No fence-sitting** ✓

---

## 4. Review (Tool / Product)

### Exemplar Structure
```markdown
# Astro 4 Review: The Content-First Framework Matures

**Meta:** An honest evaluation of Astro 4's performance, developer experience, and ecosystem readiness.

## Scoring Criteria
1. **Performance (40%)** — Build speed, bundle size, runtime overhead
2. **Developer Experience (30%)** — CLI, documentation, error messages
3. **Ecosystem (20%)** — Integrations, plugins, community support
4. **Production Readiness (10%)** — Deployment, scaling, edge cases

## Performance: 9/10
Build times for a 100-page site dropped from 12s (Astro 3) to 3s (Astro 4)...

## Developer Experience: 8/10
The new `astro dev` experience is noticeably faster. Content collections API v2 is a significant improvement...

## Ecosystem: 7/10
Still catching up to Next.js in terms of third-party integrations. The official `@astrojs/*` integrations are excellent, but community plugins are sparse...

## Production Readiness: 8/10
Deployment to Cloudflare Pages and Vercel is seamless. Image optimization is now production-grade...

## The First 5 Minutes
Installation took 45 seconds. The default starter template was well-organized. `astro dev` started immediately...

## Pros
- Exceptional build performance
- Zero JS by default
- Excellent documentation

## Cons
- Limited dynamic routing
- Smaller plugin ecosystem
- Image optimization API is verbose

## The Verdict
Astro 4 is the best choice for content-heavy websites in 2024. If you're building a marketing site, blog, or documentation, start here. If you need a fully dynamic web app, consider Next.js or Remix.
```

### What Makes This Exemplary
- **Scoring criteria defined upfront** ✓
- **The "First 5 Minutes" experience** ✓
- **Balanced pros and cons** ✓
- **The verdict** clearly states who the tool is for ✓
- **Not a rewritten press release** — includes honest criticism ✓
