const OmitMutationsPlugin = (builder) => {
    builder.hook("build", (build) => {
      const {
        pgIntrospectionResultsByKind,
      } = build;
      pgIntrospectionResultsByKind.class
        .filter(
          table =>
            table.isSelectable &&
            table.namespace
        )
        .forEach(table => {
          if (!("omit" in table.tags)) {
            table.tags.omit =
              "create,update,delete";
          }
        });
      return build;
    });
  };
  
  module.exports = OmitMutationsPlugin;