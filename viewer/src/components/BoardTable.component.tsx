import { ExternalLinkIcon, ViewIcon } from "@chakra-ui/icons";
import { Tooltip, Link, Heading, Table, Thead, Tr, Th, Tbody, Td, Box } from "@chakra-ui/react";
import { Board } from "../types";

export const BoardTable = ({ boards }: { boards: Board[] }) => {

    const renderBoardActions = (board: Board) => {
        const actions = [
          {
            label: 'View Original',
            icon: <ExternalLinkIcon />,
            href: board.board_url,
          },
          {
            label: 'View Archived',
            icon: <ViewIcon />,
            href: board.board_url,
          }
        ]
    
        return actions.map((action) => (
          <Tooltip label={action.label}>
            <Link href={action.href} target="_blank" marginX={2}>{action.icon}</Link>
          </Tooltip>
        ))
    }

    return ( 
        <Box>
            <Heading as="h2" size="lg" marginY={4}>Boards</Heading>
            <Table>
                <Thead>
                    <Tr>
                    <Th>Actions</Th>
                    <Th>Board Name</Th>
                    <Th>Threads</Th>
                    <Th>Comments</Th>
                    </Tr>
                </Thead>
                <Tbody>
                    {boards.map((board) => (
                    <Tr key={board.board_name}>
                        <Td>
                        {renderBoardActions(board)}
                        </Td>
                        <Td>{board.board_name}</Td>
                        <Td>{board.threads.length}</Td>
                        <Td>{board.threads.reduce((acc, thread) => acc + thread.comments.length, 0)}</Td>
                    </Tr>
                    ))}
                </Tbody>    
            </Table>
        </Box>
    )
};