import { Box, Text, Button, Menu } from "@chakra-ui/react";
import LANGUAGE_VERSIONS from "../constants";

const languages = Object.entries(LANGUAGE_VERSIONS);
const ACTIVE_COLOR = "blue.400";

const LanguageSelector = ({language, onSelect}) => (
  <Box ml={2} mb={4}>
    <Text mb={2} fontSize="lg">
      Language:
    </Text>
    <Menu.Root isLazy>
      <Menu.Trigger asChild>
        <Button>
          {language}
        </Button>
      </Menu.Trigger>
      <Menu.Positioner>
        <Menu.Content bg="#110c1b">
          {languages.map(([lang, version]) => (
            <Menu.Item key={lang}
            color={
                lang === language ? ACTIVE_COLOR:""
            }
            bg={
                lang === language ? "gray.900":"transparent"
            }
            _hover={{
                color:ACTIVE_COLOR,
                bg:"gray.900"
            }}
            onClick={()=>onSelect(lang)}>
              <Text as="span" mr={2}>{lang}</Text>
              <Text as="span" color="gray.600" fontSize="sm">
                ({version})
              </Text>
            </Menu.Item>
          ))}
        </Menu.Content>
      </Menu.Positioner>
    </Menu.Root>
  </Box>
);

export default LanguageSelector;
