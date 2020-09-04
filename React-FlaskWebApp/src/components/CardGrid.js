import React from 'react'
import Card from './Card'

var data = [
    { position: 'Leader', name: 'Vikas K Mahendar',phone: '+91-77081-46322', link: 'vikasmahendar2000@gmail.com' },
    { position: 'Member', name: 'Mukund Varma T',  phone: '+91-99529-51152', link: 'mukundvarmat@gmail.com' },
    { position: 'Member', name: 'Mukesh V',        phone: '+91-80568-36775', link: 'mukeshvinayak2001@gmail.com' },
]

function CardGrid() {
    return (
        <footer>
            <div style={{
                display: 'flex',
                flexDirection: 'row',
                justifyContent: 'center',
                bottom: '4px'
            }}>
                {
                    data.map((item, key) => {
                        return <Card data={item} key={key} />
                    })
                }
            </div>
        </footer>
    )
}

export default CardGrid