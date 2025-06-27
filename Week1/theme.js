// theme.js
import { createSystem, defaultConfig } from "@chakra-ui/react";

const system = createSystem(defaultConfig, {
  config: {
    initialColorMode: "dark",
    useSystemColorMode: false,
  },
  // Add other theme customizations here if needed
});

export default system;
