import { Divider, Box, Text, Heading, HStack } from "@chakra-ui/react"
import { ForumData, ForumStats } from "../types"

export const Header = ({ stats, crawledAt }: { stats: ForumStats, crawledAt: string }) => { 
    return (
        <>
            <HStack justify="space-between" alignItems="center">
            <Box>
                <Heading as="h1" size="2xl">
                    223 Historical Archives
                </Heading>
                <Text>Unproudly vibe coded by antican</Text>
            </Box>
            <Box>
                <Text>Crawled at {new Date(crawledAt).toLocaleString()}</Text>
                <Text>
                    {stats.boards_discovered} boards, {` `}
                    {stats.threads_discovered} threads, {` `}
                    {stats.comments_extracted} comments
                </Text>
            </Box>
            </HStack>
            <Divider marginY={4} />
        </>
    )
}