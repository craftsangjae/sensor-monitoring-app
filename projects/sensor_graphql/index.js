const express = require("express");
const { postgraphile } = require("postgraphile");
const PgAggregatesPlugin = require("@graphile/pg-aggregates").default;
const OmitMutationsByDefaultPlugin = require("./plugins/omitMutations");
const TimeScaleAggregateGroupSpecsPlugin = require("./plugins/timeScaleAggregates");
const { Pool } = require('pg');

const app = express();

const DATABASE_URL = process.env.DATABASE_URL || "postgres://user:pass@host:5432/dbname"

const pool = new Pool({connectionString: DATABASE_URL, max: 1});

app.get('/health', async (req, res) => {
    try {
      await pool.query('SELECT 1');
      res.json({status: 'healthy'});
    } catch (error) {
      res.status(503).json({
        status: 'unhealthy', error: error.message
      });
    }
  });

app.use(
  postgraphile(
    DATABASE_URL,
    "public",
    {
      watchPg: process.env.ENV !== "production",
      graphiql: true,
      allowExplain: process.env.ENV !== "production",  
      enhanceGraphiql: true,
      appendPlugins: [
        require("@graphile-contrib/pg-simplify-inflector"),
        PgAggregatesPlugin,
        OmitMutationsByDefaultPlugin,
        TimeScaleAggregateGroupSpecsPlugin,
      ]
    }
  )
);

console.log(`Server is running on port ${process.env.PORT || 3000}`);
app.listen(process.env.PORT || 3000);