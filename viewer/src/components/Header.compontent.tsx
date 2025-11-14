import {
  Divider,
  Box,
  Text,
  Heading,
  Select,
  HStack,
  VStack,
  Tooltip,
  Button,
} from "@chakra-ui/react";
import { Archive } from "../types";
import { useCallback, useRef } from "react";
import { DownloadIcon } from "@chakra-ui/icons";

export const Header = ({
  archives,
  selectedArchive,
  setSelectedArchive,
}: {
  archives: Archive[];
  selectedArchive: Archive;
  setSelectedArchive: (archive: Archive) => void;
}) => {
  const downloadLinkRef = useRef<HTMLAnchorElement>(null);

  const handleArchiveSelect = useCallback(
    (event: React.ChangeEvent<HTMLSelectElement>) => {
      const selectedArchive = archives.find(
        (archive) => archive.filename === event.target.value
      );
      if (selectedArchive) {
        setSelectedArchive(selectedArchive);
      }
    },
    [archives, setSelectedArchive]
  );

  const handleDownloadArchive = useCallback(
    async () => {
      const archive = archives.find(
        (archive) => archive.filename === selectedArchive?.filename
      );
      if (!archive || !downloadLinkRef.current) return;

      try {
        const response = await fetch(`http://localhost:5000/${archive.filepath}`);
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);

        downloadLinkRef.current.href = url;
        downloadLinkRef.current.download = archive.filename;
        downloadLinkRef.current.click();

        window.URL.revokeObjectURL(url);
      } catch (error) {
        console.error('Failed to download archive:', error);
      }
    }, [archives, selectedArchive]
  );

  return (
    <>
      <a ref={downloadLinkRef} style={{ display: 'none' }} />
      <HStack justify="space-between" alignItems="center">
        <Box>
          <Heading as="h1" size="2xl">
            223 Historical Archives
          </Heading>
        </Box>
        <Box>
          <VStack align="flex-start">
            <Text fontSize="sm" color="gray.500" fontWeight="900">
              Select An Archive
            </Text>
            <HStack>
              <Select onChange={handleArchiveSelect}>
                {archives.map((archive) => {
                  const prettyDate = new Date(
                    archive.crawled_at
                  ).toLocaleString();
                  const label = `${prettyDate} - ${archive.stats.boards} boards, ${archive.stats.threads} threads, ${archive.stats.comments} comments`;

                  return (
                    <option key={archive.crawled_at} value={archive.filename}>
                      {label}
                    </option>
                  );
                })}
              </Select>
              <Tooltip label="Download Archive (JSON)">
                <Button onClick={handleDownloadArchive}>
                  <DownloadIcon />
                </Button>
              </Tooltip>
            </HStack>
          </VStack>
        </Box>
      </HStack>
      <Divider marginY={4} />
    </>
  );
};
