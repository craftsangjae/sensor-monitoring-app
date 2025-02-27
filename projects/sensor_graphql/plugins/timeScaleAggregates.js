const TimeScaleAggregateGroupSpecsPlugin = (builder) => {
    builder.hook("build", (build) => {
      const { pgSql: sql } = build;
  
      build.pgAggregateGroupBySpecs = [
        ...build.pgAggregateGroupBySpecs,
        {
          id: "time-bucket-hour",
          isSuitableType: type => type.name === "timestamptz",
          sqlWrap: (sqlFrag) => sql.fragment`time_bucket('1 hour', ${sqlFrag})`
        },
        {
          id: "time-bucket-day",
          isSuitableType: type => type.name === "timestamptz",
          sqlWrap: (sqlFrag) => sql.fragment`time_bucket('1 day', ${sqlFrag})`
        }
      ];
  
      return build;
    });
  };
  
  module.exports = TimeScaleAggregateGroupSpecsPlugin;