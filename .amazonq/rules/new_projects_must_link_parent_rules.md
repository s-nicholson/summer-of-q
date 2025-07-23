When creating a new project (subdirectory) under `summer-of-q`, always create a symlink to the parent rules.

Steps:
1. Create `.amazonq` directory in the new project
2. Create a symlink to the parent rules directory:
   ```
   ln -s ../../.amazonq/rules new-project/.amazonq/rules
   ```

This ensures all projects automatically inherit and follow the parent rules.
