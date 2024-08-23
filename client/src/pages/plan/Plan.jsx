// Imports
import { useState } from "react";
import { Link } from "react-router-dom";

// Styling
import "./Plan.scss";

// Utils
import { formatDate } from "../../utils/formatter"

// Components
import ResourceDistributionMap from "../../components/resourceDistributionMap/ResourceDitributionMap";
import Trucks from "../../components/trucks/Trucks";
import Containers from "../../components/containers/Containers";
import Orders from "../../components/orders/Orders";
import TaskjobMap from "../../components/taskjobMap/TaskjobMap";

export default function Plan() {
    const [groupedTasks, setGroupedTasks] = useState([
        {
            "TaskJobID": "1",
            "OrderID": 1,
            "TaskJobType": "Book_1",
            "Deadline": "2024-04-25",
            "Locations": [null, 13],
        },
        {
            "TaskJobID": "2",
            "OrderID": 1,
            "TaskJobType": "Book_2",
            "Deadline": "2024-04-30",
            "Locations": [13, 17],
        },
        {
            "TaskJobID": "3",
            "OrderID": 2,
            "TaskJobType": "Bill_1",
            "Deadline": "2024-07-10",
            "Locations": [19, 11],
        },
        {
            "TaskJobID": "4",
            "OrderID": 2,
            "TaskJobType": "Bill_2",
            "Deadline": "2024-07-20",
            "Locations": [11, 19],
        },
        {
            "TaskJobID": "3",
            "OrderID": 3,
            "TaskJobType": "Bill_1",
            "Deadline": "3024-07-10",
            "Locations": [19, 11],
        },
        {
            "TaskJobID": "4",
            "OrderID": 3,
            "TaskJobType": "Bill_2",
            "Deadline": "2024-07-20",
            "Locations": [11, 19],
        }
    ]);

    const [selectedOrderID, setSelectedOrderID] = useState(null);

    // Group tasks by OrderID
    const groupedByOrder = groupedTasks.reduce((acc, task) => {
        if (!acc[task.OrderID]) {
            acc[task.OrderID] = [];
        }
        acc[task.OrderID].push(task);
        return acc;
    }, {});

    return (
        <div className="overview plan">
            <h1>
                <Link to="/" className="btn back-btn mr-12">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="size-6">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M9 15 3 9m0 0 6-6M3 9h12a6 6 0 0 1 0 12h-3" />
                    </svg>
                </Link>

                Dispatching Plan
                <hr />
            </h1>

            {/* Trucks */}
            <div className="overview--left plan--left">
                <div className="insight-container mt-12">
                    <div className="insight-item">
                        <strong>Taskjobs assigned</strong>
                        <p>{groupedTasks.length}</p>
                    </div>
                    <div className="insight-item">
                        <strong>Distance cost</strong>
                        <p>44.36km</p>
                    </div>
                    <div className="insight-item">
                        <strong>Trucks assigned</strong>
                        <p>10</p>
                    </div>
                    <div className="insight-item">
                        <strong>Containers assigned</strong>
                        <p>01</p>
                    </div>
                </div>

                <br />
                <div className="order-container">
                    {Object.keys(groupedByOrder).map(orderID => (
                        <div
                            className={`order-item ${selectedOrderID === orderID ? 'active' : ''}`}
                            key={orderID}
                            onClick={() => setSelectedOrderID(orderID)}
                        >
                            <h2>Order ID: {orderID}</h2>
                            <hr />
                            <div className="order-item__step-container">
                                {groupedByOrder[orderID].map(task => (
                                    <div key={task.TaskJobID} className="order-item__step-item">
                                        <strong>TaskJob {task.TaskJobID?.padStart(2, 0)}: </strong> {task.Locations[0]} - {task.Locations[1]}<br />
                                        <strong>Type:</strong> {task?.TaskJobType?.includes("Book") ? "Booking" : "Billing"}<br />
                                        <strong>Deadline:</strong> {formatDate(task.Deadline)}<br />
                                    </div>
                                ))}
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            <div className="overview--right">
                <TaskjobMap />
            </div>
        </div>
    );
}