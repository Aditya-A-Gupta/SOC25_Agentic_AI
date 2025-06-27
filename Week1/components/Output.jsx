import { Box, Button, Text } from "@chakra-ui/react";
import { useState } from "react";
import { executeCode } from "../api";

const Output = ({ editorRef, language }) => {
    const [output, setOutput] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [isError, setIsError] = useState(false);

    const runCode = async () => {
        const sourceCode = editorRef.current.getValue();
        if (!sourceCode) return;
        try {
            setIsLoading(true);
            const { run: result } = await executeCode(language, sourceCode);
            setOutput((result.output || "").split("\n"));
            setIsError(!!result.stderr);
        } catch (error) {
            setIsError(true);
            setOutput(["An error occurred while running the code."]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Box w='50%'>
            <Text mb={2} fontSize='lg'>Output</Text>
            <Button
                variant='outline'
                colorScheme='green'
                mb={4}
                onClick={runCode}
                isLoading={isLoading}
            >
                Run Code
            </Button>
            <Box
                height='75vh'
                p={2}
                color={isError ? "red.400" : "inherit"}
                border='1px solid'
                borderRadius={4}
                borderColor={isError ? "red.500" : '#333'}
            >
                {output.length > 0
                    ? output.map((line, i) => <Text key={i}>{line}</Text>)
                    : 'Click "Run Code" to see output'
                }
            </Box>
        </Box>
    );
};

export default Output;
