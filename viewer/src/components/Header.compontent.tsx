import {
  Divider,
  Box,
  Text,
  Heading,
  Select,
  HStack,
  VStack,
} from "@chakra-ui/react";
import { Archive } from "../types";
import { useCallback } from "react";

export const Header = ({
  archives,
  setSelectedArchive,
}: {
  archives: Archive[];
  setSelectedArchive: (archive: Archive) => void;
}) => {
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

  return (
    <>
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
          </VStack>
        </Box>
      </HStack>
      <Divider marginY={4} />
    </>
  );
};
