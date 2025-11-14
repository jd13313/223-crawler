import {
  Center,
  Container,
  Spinner,
  Text,
} from '@chakra-ui/react'

import { Archive, ForumData } from './types';
import { BoardTable } from './components/BoardTable.component';
import { Header } from './components/Header.compontent';
import { useEffect, useState } from 'react';

function App() {
  const [archives, setArchives] = useState<Archive[] | null>(null);
  const [selectedArchive, setSelectedArchive] = useState<Archive | null>(null);
  const [forumData, setForumData] = useState<ForumData | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!archives) {
      fetch('http://localhost:5000/archives')
        .then(response => response.json())
        .then(data => {
          setArchives(data.archives)
          setSelectedArchive(data.archives[0])
        })
        .then(() => setIsLoading(false))
        .catch(error => console.error('Error fetching forum data:', error));
    }
  }, []);

  useEffect(() => {
    if (selectedArchive) {
      fetch(`http://localhost:5000/archives/${selectedArchive.filename}`)
        .then(response => response.json())
        .then(data => setForumData(data))
        .then(() => setIsLoading(false))
        .catch(error => console.error('Error fetching forum data:', error));
    }
  }, [selectedArchive]);


  return (
    <Container maxW="100vw" h="100vh" py={8}>
      {isLoading && (
        <Center>
          <Spinner size="xl" />
        </Center>
      )}
      {archives && (
        <Header archives={archives} selectedArchive={selectedArchive ?? archives[0]} setSelectedArchive={setSelectedArchive} />
      )}
      {forumData && (
        <BoardTable boards={forumData.boards} />
      )}
    </Container>
  )
}

export default App

