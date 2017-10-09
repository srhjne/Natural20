"use strict";


class ContentBox extends React.Component {
	constructor(props) {
        super(props);
        this.state = {
            team_members: {},
            teams: [],
        };
    }

     render() {
        return (
            <div className="container-fluid">
                <div className="row">
                    <div className="col-sm-3 col-xs-12 teams">
                    	<TeamList> </TeamList>
                        
                    </div>
                    <div className="col-sm-9 col-xs-12 my-team">
                        My team testing
                    </div>
                </div>
            </div>
        );
	}

}

class TeamList extends React.Component {

	render() {
		return (
			<h1> Team List </h1>
		)
	}
	


}

ReactDOM.render(
    <ContentBox />,
    document.getElementById("content")
);