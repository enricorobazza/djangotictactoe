import React, {useEffect, useState, useRef} from 'react';
import ReactDOM from 'react-dom';
import Cell from '../components/cell';

const Index = (props) => {
    const [turn, setTurn] = useState(false);
    const userSocket = useRef(null);
    const roomSocket = useRef(null);
    const [matrix, setMatrix] = useState([]);
    const [gameOver, setGameOver] = useState(false);
    const [victory, setVictory] = useState(false);

    const uniqueID = () => {
        return (Date.now().toString(36) + Math.random().toString(36).substr(2, 5)).toUpperCase()
    }

    const updateStatus = (status) => {
        const {matrix: __matrix, turn, gameOver: _gameOver, victory: _victory } = status;
        console.log(status);
        setMatrix(__matrix);
        setTurn(turn);
        setGameOver(_gameOver);
        setVictory(_victory);
    }

    useEffect(() => {
        const roomName = JSON.parse(document.getElementById('room-name').textContent);
        const id = uniqueID();
        userSocket.current = new WebSocket(`ws://${window.location.host}/ws/me/${id}/`);
        roomSocket.current = new WebSocket(`ws://${window.location.host}/ws/tictactoe/${roomName}/${id}/`);

        userSocket.current.onmessage = function(e) {
            const data = JSON.parse(e.data);

            if(data.type === "status" && !data.connect){
                roomSocket.current.close();
                userSocket.current.close();
                alert(data.message);
                window.location.href = '/';
            }

            else if(data.type === "game_status"){
                const {status} = data;
                updateStatus(status);
            }
        };

        roomSocket.current.onmessage = function(e) {
            const {status} = JSON.parse(e.data);
            updateStatus(status);
        };

    }, [])

    const resetGame = () => {
        roomSocket.current.send(JSON.stringify({
            'reset': true
        }));
    }

    const cellClick = (e, i, j) => {
        if(e.target.value === "") return;
        if(!turn) return;

        roomSocket.current.send(JSON.stringify({
            'i': i,
            'j': j
        }));
    }

    return (
        <div>
            {!gameOver ?
                <>
                    <table>
                        {matrix.map((row, i) => (
                            <tr>
                                {row.map((cell, j) => (
                                    <Cell 
                                        onClick={(e) => cellClick(e, i, j)} 
                                        value={cell}
                                    />
                                ))}
                            </tr>
                        ))}
                    </table>
                    <div>{turn ? "Seu turno" : "Esperar oponente"}</div>
                </>
            : (
                <div>
                    Fim de Jogo! {victory ? "Você venceu!!" : "Você perdeu!!"}
                    <button onClick={resetGame}>Jogar novamente</button>
                </div>
            )}
        </div>
    )
}

let props;

try{
    props = {...context}
}
catch(err){
    props = {}
}


ReactDOM.render(<Index {...props}></Index>, document.getElementById('root'));;