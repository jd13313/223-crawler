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
import { BoardTable } from './components/BoardTable.component';
import { Header } from './components/Header.compontent';

function App() {
  const forumData = forumDataJson as ForumData;



  return (
    <Container maxW="container.xl" py={8}>
        <Header stats={forumData.stats} crawledAt={forumData.crawled_at} />
        <BoardTable boards={forumData.boards} />
    </Container>
  )
}

export default App

