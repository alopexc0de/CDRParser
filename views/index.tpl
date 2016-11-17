<!DOCTYPE html>
<html ng-app="MyApp">
<head>
    <meta charset="utf-8" />
    <title>Cisco CDR Viewer</title>
    <link rel="stylesheet" type="text/css" href="/static/css/angular-material.min.css" />
    <link rel="stylesheet" type="text/css" href="/static/css/logview.css" />
    <link rel="stylesheet" type="text/css" href="/static/css/tablesort.css" />

    <!-- Put JS in head to support cloak before load -->
    <script src="/static/js/angular.min.js"></script>
    <script src="/static/js/angular-animate.min.js"></script>
    <script src="/static/js/angular-aria.min.js"></script>
    <script src="/static/js/angular-material.min.js"></script>
    <script src="/static/js/angular-tablesort.js"></script>
    <script src="/static/js/controller.js"></script>

</head>
<body ng-controller="logviewer" ng-cloak>

    <div flex layout="column">
        <md-toolbar class="md-menu-toolbar">
            <div class="md-toolbar-tools">
                <span flex class="nav">
                <md-button href=""></md-button> <!-- these are basically just anchors, but can have md-icon, md-tooltip, etc inside them-->
                <md-button href=""></md-button>
                </span>
            </div>
        </md-toolbar>

        <md-card>
            <md-toolbar class="md-table-toolbar" style="background: #f5f5f5;color: rgba(0,0,0,0.87);">
                <div class="md-toolbar-tools layout-row">
                    <h2 class="md-title">Cisco CDR Phone Logs for [[page]]</h2>
                    <span flex></span>
                    <md-input-container style="margin-top:1.4rem;">
                        <label>Call Origin</label>
                        <md-select ng-model="query.origin">
                            <md-option ng-value="opt" ng-repeat="opt in origins">{{opt}}</md-option>
                        </md-select>
                    </md-input-container>
                    <md-input-container>
                        <label>Username</label>
                        <input type="text" ng-model="query.username" ng-model-options="{debounce: 500}">
                    </md-input-container>
                    <md-input-container>
                        <label>Call From</label>
                        <input type="text" ng-model="query.from" ng-model-options="{debounce: 500}">
                    </md-input-container>
                    <md-input-container>
                        <label>Call To</label>
                        <input type="text" ng-model="query.to" ng-model-options="{debounce: 500}">
                    </md-input-container>
                    <md-button class="resetbtn" ng-click="resetquery()">
                        Clear Search
                    </md-button>
                </div>
            </md-toolbar>
            <center>
                <table ts-wrapper>
                    <thead>
                        <tr>
                            <th class="count">Count</th>
                            <th ts-criteria='connect'>Start Time</th>
                            <th ts-criteria='disconnect'>Stop Time</th>
                            <th ts-criteria='origin'>Call Origin</th>
                            <th ts-criteria='username'>Username</th>
                            <th ts-criteria='calling'>Call From</th>
                            <th ts-criteria='called'>Call To</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr ng-repeat="d in data track by $index" ts-repeat>
                            <td>{{$index}}</td>
                            <td ng-value="d.connect">{{d.connect | date:'MM-dd-yyyy HH:mm-ss'}}</td>
                            <td ng-value="d.disconnect">{{d.disconnect | date:'MM-dd-yyyy HH:mm-ss'}}</td>
                            <td ng-value="d.origin">{{d.origin}}</td>
                            <td ng-value="d.username">{{d.username}}</td>
                            <td ng-value="d.calling">{{d.calling}}</td>
                            <td ng-value="d.called">{{d.called}}</td>
                        </tr>
                    </tbody>
                </table>
            </center>
        </md-card>
    </div>
</body>
</html>