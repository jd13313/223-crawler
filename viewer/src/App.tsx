import {
  Container,
  Heading,
  Text,
  Box,
  Divider,
  HStack,
  VStack,
  Table,
  Thead,
  Tr,
  Th,
  Td,
  Tbody,
  Link,
  Tooltip,
} from '@chakra-ui/react'
import forumDataJson from '../../forum_data.json'
import { Board, ForumData } from './types';
import { ExternalLinkIcon, ViewIcon } from '@chakra-ui/icons';
import { BoardTable } from './components/BoardTable/BoardTable.component';

function App() {
  const forumData = forumDataJson as ForumData;



  return (
    <Container maxW="container.xl" py={8}>
        <HStack justify="space-between" alignItems="center">
          <Box>
            <Heading as="h1" size="2xl">
              223 Historical Archives
            </Heading>
            <Text>Unproudly vibe coded by antican</Text>
          </Box>
          <Box>
            <Text>Crawled at {new Date(forumData.crawled_at).toLocaleString()}</Text>
            <Text>{forumData.stats.boards_discovered} boards, {forumData.stats.threads_discovered} threads, {forumData.stats.comments_extracted} comments</Text>
          </Box>
        </HStack>
        <Divider marginY={4} />
        <BoardTable boards={forumData.boards} />
    </Container>
  )
}

export default App

