import React, {useEffect, useState, useRef} from 'react';

const Cell = ({value, onClick }) => {
    const [recentlyInserted, setRecentlyInserted] = useState(true);
    const cellContainer = useRef(null);

    useEffect(() => {

        if(value === "") return;

        if(cellContainer.current.innerHTML === "") {
            cellContainer.current.classList.add('empty');
            setTimeout(() => {
                cellContainer.current.classList.remove('empty');
            }, 5)
        }

        cellContainer.current.innerHTML = value;

    }, [value])

    return <td className="empty" ref={cellContainer} onClick={onClick}></td>
}

export default Cell;