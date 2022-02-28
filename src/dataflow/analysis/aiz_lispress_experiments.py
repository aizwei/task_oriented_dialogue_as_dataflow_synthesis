#!/usr/bin/env python3

import argparse
from typing import List
import os

from dataflow.core.dialogue import Dialogue, Turn
from dataflow.core.io_utils import load_jsonl_file
from dataflow.core.lispress import Lispress, lispress_to_program, parse_lispress, render_pretty
from dataflow.core.program import BuildStructOp, ValueOp, CallLikeOp, Expression, Program
from dataflow.core.sexp import LEFT_PAREN, RIGHT_PAREN
"""
Sample usage:
➜  output git:(master) ✗ python src/dataflow/analysis/aiz_lispress_experiments.py \
    --dataflow_dialogues_dir ${dataflow_dialogues_dir} \
    --subset first_dialogue \
    --outdir ${dataflow_dialogues_stats_dir}

args:
dataflow_dialogues_dir - directory which contains dataset
subset - name of dataset to test on, passing "first_dialogue" will look for the file first_dialogue.dataflow_dialogues.jsonl, this is copied from their instructions in the README
outdir - output directory to write result files to
"""

def convert_lispress_to_python(dataflow_dialogues: List[Dialogue]):
    for dialogue in dataflow_dialogues:
        print(f"looking at dialogue: {dialogue} \n\n")

        for turn in dialogue.turns:
            turn: Turn
            print("\n")
            print(f"printing turn: {turn}")
            print(f"PRINTING LISPRESS FOR TURN")
            # TODO: render_pretty doesnt seem to be printing in the format I expect here,
            # it is still all contained in one line
            print(render_pretty(turn.lispress))
            lispress: Lispress = parse_lispress(s=turn.lispress)

            print("\n")
            for l in turn.tokenized_lispress():
                print(f"next token looks like {l}")

            print("\n")

            program_object: Program = lispress_to_program(lispress=lispress, idx=0)[0]
            print(f"resulting program object is {program_object.expressions_by_id}")

            # built in function which will do this for us:
            program: Program = turn.program()
            print(f"{program}")

            tokenlized_lispress = turn.tokenized_lispress()
            print(f"{tokenlized_lispress}")


            # alternatively, we can use their built-in try round trip to check for valid lispress
            # the specific exception is swallowed when there are issues though
            #result_of_round_trip = try_round_trip(lispress_str=lispress_string)

            #print(f"result of round trip is {result_of_round_trip}")

def extract_library_functions(dataflow_dialogues: List[Dialogue]):

    """
    output running this function on the full smcalflo - 2.0 dataset:
    Reading <class 'dataflow.core.dialogue.Dialogue'> from output/dataflow_dialogues/train.dataflow_dialogues.jsonl: 32593 dialogues [00:44, 736.58 dialogues/s]


    PRINTING UNIQUE BUILD STRUCT OPS
    {'NextWeekend', 'Holiday.AshWednesday', 'OnDateBeforeTime', 'Afew', 'LastYear', 'December', 'HourMinuteAm', 'Date.dayOfWeek_?', 'Event.id', 'ChooseUpdateEventFromConstraint', 'FullMonthofPreviousMonth', 'ChoosePersonFromConstraint', 'RespondShouldSend.apply', 'Event.organizer_?', 'TimeToTime', 'ShowAsStatus.Unknown', 'IsCloudy', 'AttendeeType.Required', 'Path.apply', 'Early', 'Event.responseStatus', 'FenceAttendee', 'DateTime.date_?', 'Holiday.GoodFriday', 'WeatherQuantifier.Sum', 'PersonName.apply', 'Weekend', 'TimeAfterDateTime', 'AlwaysFalseConstraint', 'Latest', 'WillRain', 'Morning', 'WeatherPleasantry', 'List.apply', 'Person.phoneNumber', 'AttendeeType.Optional', 'UpdatePreflightEventWrapper', 'FenceOther', 'Place.price', 'Execute', 'Event.start', 'WeekendOfMonth', 'ThisWeekend', 'SeasonSpring', 'Midnight', 'Place.hours', 'Here', 'FindLastEvent', 'WeatherQuantifier.Average', 'AttendeeListExcludesRecipient', 'IsCold', 'LastPeriod', 'Weekdays', 'Holiday.Kwanzaa', 'Event.attendees', 'Holiday.ValentinesDay', 'ConfirmCreateAndReturnAction', 'EventOnDateTime', 'EmptyStructConstraint', 'NextYear', 'DateAtTimeWithDefaults', 'PlaceFeature.GoodforGroups', 'PersonFromRecipient', 'CreatePreflightEventWrapper', 'Event.end_?', 'WeatherAggregate', 'UpdateEventIntensionConstraint', 'Event.end', 'Holiday.MemorialDay', 'BottomResult', 'HourMinuteMilitary', 'GenericPleasantry', 'FindEventWrapperWithDefaults', 'HourMinutePm', 'Holiday.BlackFriday', 'Yield', 'LateMorning', 'AroundDateTime', 'DateTime.time_?', 'Event.organizer', 'AttendeeListHasPeople', 'EarlyTimeRange', 'FindTeamOf', 'FindReports', 'PeriodDurationBeforeDateTime', 'Holiday.PresidentsDay', 'ShowAsStatus.Free', 'Event.isOneOnOne_?', 'Event.duration_?', 'Holiday.Thanksgiving', 'HolidayYear', 'NextMonth', 'PlaceFeature.HappyHour', 'WillSleet', 'EventAtTime', 'NextTime', 'ShowAsStatus.Busy', 'ShowAsStatus.OutOfOffice', 'EarlyDateRange', 'Year.apply', 'Holiday.MardiGras', 'NextHolidayFromToday', 'Holiday.NewYearsEve', 'OnDateAfterTime', 'FullYearofYear', 'DeletePreflightEventWrapper', 'EventRescheduled', 'NeedsJacket', 'IsHot', 'IsSunny', 'UserPauseResponse', 'EventAllDayOnDate', 'ThisWeek', 'DateTimeConstraint', 'EventOnDateAfterTime', 'FenceComparison', 'Place.url', 'NewClobber', 'EventDuringRange', 'August', 'SeasonSummer', 'Person.officeLocation', 'IsTeamsMeeting', 'DateTime.time', 'Saturday', 'Wednesday', 'EventBeforeDateTime', 'EventOnDateFromTimeToTime', 'MonthDayToDay', 'Late', 'WhenProperty', 'Event.start_?', 'FindPlace', 'EventDuringRangeDateTime', 'IsSnowy', 'AlwaysTrueConstraint', 'FenceSwitchTabs', 'SeasonFall', 'EventOnDateBeforeTime', 'CreateCommitEvent.data_?', 'DeleteCommitEventWrapper', 'QueryEventResponse.results', 'AttendeeListHasPeopleAnyOf', 'DoNotConfirm', 'AttendeeListHasRecipientWithType', 'Holiday.TaxDay', 'PeriodBeforeDate', 'FenceConditional', 'Holiday.GroundhogDay', 'Evening', 'ResponseStatusType.Accepted', 'PlaceHasFeature', 'Holiday.AprilFoolsDay', 'NextDOW', 'Holiday.MothersDay', 'SetOtherOrganizer', 'Holiday.Easter', 'ChooseUpdateEvent', 'TimeBeforeDateTime', 'PlaceFeature.Casual', 'AttendeesWithResponse', 'TimeSinceEvent', 'FencePlaces', 'ForwardEventWrapper', 'FenceDateTime', 'DateTime.date', 'ResponseStatus.response', 'FindNumNextEvent', 'ActionIntensionConstraint', 'March', 'Future', 'ShowAsStatus.Tentative', 'ClosestDayOfWeek', 'Brunch', 'Holiday.VeteransDay', 'ResponseStatusType.None', 'IsFree', 'Date.day_?', 'Holiday.LaborDay', 'FenceNavigation', 'EndOfWorkDay', 'AttendeesWithNotResponse', 'Date.month', 'September', 'Event.duration', 'ConfirmDeleteAndReturnAction', 'FenceWeather', 'FenceRecurring', 'NumberWeekOfMonth', 'LateDateRange', 'ChooseCreateEvent', 'WillSnow', 'Holiday.EasterMonday', 'Yesterday', 'AttendeeListHasRecipient', 'Now', 'Holiday.Christmas', 'PleasantryCalendar', 'EventBetweenEvents', 'PlaceFeature.FullBar', 'DowOfWeekNew', 'Holiday.IndependenceDay', 'ConvertTimeToAM', 'DowToDowOfWeek', 'Date.year', 'WeekOfDateNew', 'Holiday.FathersDay', 'NumberInDefaultTempUnits', 'FenceTeams', 'IsWindy', 'Holiday.MLKDay', 'Today', 'FenceGibberish', 'Holiday.ColumbusDay', 'July', 'PersonWithNameLike', 'QueryEventIntensionConstraint', 'ConstraintTypeIntension', 'DateTimeFromDowConstraint', 'Event.isAllDay_?', 'LastWeekNew', 'Holiday.FlagDay', 'EventAllDayDateUntilDate', 'Event.location_?', 'LastWeekendOfMonth', 'EventAttendance', 'NumberPM', 'June', 'PleasantryAnythingElseCombined', 'Day.apply', 'Later', 'RecipientFromRecipientConstraint', 'Event.location', 'CurrentUser', 'Place.phoneNumber', 'MDY', 'ChooseCreateEventFromConstraint', 'Friday', 'Person.emailAddress', 'LateAfternoon', 'FindPlaceMultiResults', 'FenceConferenceRoom', 'EventAllDayForDateRange', 'Date.dayOfWeek', 'PlaceDescribableLocation', 'Holiday.EarthDay', 'IsBusy', 'TimeAround', 'Event.attendees_?', 'CancelScreen', 'NextWeekList', 'EventSpec.attendees_?', 'Earliest', 'Acouple', 'AttendeeFromEvent', 'AttendeeResponseStatus', 'NextPeriodDuration', 'AgentStillHere', 'FenceReminder', 'May', 'Event.showAs', 'FindManager', 'EventDuringRangeTime', 'LastDuration', 'ClosestDay', 'FencePeopleQa', 'RespondComment.apply', 'FullMonthofLastMonth', 'EventForRestOfToday', 'IsHighUV', 'DateTimeAndConstraintBetweenEvents', 'PeriodDuration.apply', 'Date.month_?', 'UpdateCommitEventWrapper', 'FenceMultiAction', 'Holiday.StPatricksDay', 'ConvertTimeToPM', 'Event.showAs_?', 'Thursday', 'DateAndConstraint', 'PlaceFeature.OutdoorDining', 'Monday', 'WeatherQuantifier.Min', 'ConfirmUpdateAndReturnActionIntension', 'Holiday.PatriotDay', 'Place.rating', 'Holiday.PalmSunday', 'EventSpec.start_?', 'WeatherQueryApi', 'Holiday.NewYearsDay', 'CreateCommitEventWrapper', 'EventOnDate', 'Sunday', 'Tuesday', 'ShowAsStatus.WorkingElsewhere', 'FullMonthofMonth', 'November', 'PlaceFeature.WaiterService', 'Noon', 'RecipientWithNameLike', 'Night', 'April', 'PlaceSearchResponse.results', 'Holiday.ElectionDay', 'LastDayOfMonth', 'PlaceFeature.FamilyFriendly', 'WeatherForEvent', 'GreaterThanFromStructDateTime', 'List.Nil', 'FenceScope', 'Dinner', 'Event.id_?', 'Date.day', 'ResponseStatusType.Declined', 'AtPlace', 'January', 'AttendeeListHasRecipientConstraint', 'NumberWeekFromEndOfMonth', 'LessThanFromStructDateTime', 'Event.subject', 'HourMilitary', 'MD', 'NextPeriod', 'Lunch', 'FindPlaceAtHere', 'WeekendOfDate', 'NumberAM', 'EventOnDateWithTimeRange', 'EventAfterDateTime', 'RecipientAvailability', 'ClosestMonthDayToDate', 'ReviseConstraint', 'Afternoon', 'SeasonWinter', 'February', 'ResponseStatusType.TentativelyAccepted', 'EventAllDayStartingDateForPeriod', 'RepeatAgent', 'DateTimeAndConstraint', 'Event.subject_?', 'October', 'FenceTriviaQa', 'EventSometimeOnDate', 'Place.formattedAddress', 'FenceSpecify', 'ResponseStatusType.NotResponded', 'FenceAggregation', 'ConfirmAndReturnAction', 'Tomorrow', 'Breakfast', 'PersonOnTeam', 'TopResult', 'IsStormy', 'LateTimeRange', 'Holiday.Halloween', 'WeatherQuantifier.Max', 'PlaceFeature.Takeout', 'WeatherQuantifier.Summarize', 'LocationKeyphrase.apply', 'IsRainy'}
    total count is 360
    
    total count of value ops is 23100


    PRINTING CALL LIKE OPS
    {'nextDayOfMonth', 'rainPrecipProbability', 'toFourDigitYear', '?>', 'item', 'addPeriodDurations', 'or', 'pressure', 'listSize', 'snowPrecipIntensity', 'cursorNext', 'toSeconds', 'previousHoliday', 'toHours', 'inFahrenheit', '<=', '>', 'windBearing', 'toMonth', '>=', 'exists', 'sunriseTime', 'append', 'windSpeed', 'toFahrenheit', 'singleton', 'nextDayOfWeek', '?~=', 'precipProbability', 'orConstraint', '-', '?<=', 'nextMonthDay', 'size', 'toMonths', 'snowPrecipAccumulation', 'toYears', 'addDurations', '?<', 'alwaysTrueConstraintConstraint', 'rainPrecipIntensity', 'adjustByPeriod', 'negate', 'takeRight', 'sunsetTime', 'roomRequest', 'adjustByPeriodDuration', 'numberToIndexPath', 'previousDayOfWeek', 'cloudCover', 'toRecipient', 'joinEventCommand', 'roleConstraint', 'toDays', 'apparentTemperature', 'cursorPrevious', 'previousDayOfMonth', 'toWeeks', 'allows', 'not', '?>=', 'previousMonthDay', 'toMinutes', 'inCelsius', '&', 'addPeriods', '==', 'subtractDurations', 'temperature', 'intension', 'extensionConstraint', 'visibility', 'snowPrecipProbability', '+', 'uvIndex', 'humidity', 'take', 'longToNum', 'dewPoint', 'do', '?=', 'adjustByDuration', 'refer', 'inInches', '<', 'inUsMilesPerHour', 'nextHoliday'}
    total count is 87
        
    """
    unique_build_struct_ops = set()
    unique_value_ops = set()
    unique_call_like_ops = set()
    for dialogue in dataflow_dialogues:
        for turn in dialogue.turns:
            turn: Turn
            # tokenlized_lispress = turn.tokenized_lispress()
            # for token in tokenlized_lispress:
            #     if token is not LEFT_PAREN and token is not RIGHT_PAREN:
            #         unique_tokens.add(token)
            program: Program = turn.program()
            for _, e in program.expressions_by_id.items():
                e: Expression
                if isinstance(e.op, BuildStructOp):
                    unique_build_struct_ops.add(e.op.op_schema)
                elif isinstance(e.op, ValueOp):
                    unique_value_ops.add(e.op.value)
                elif isinstance(e.op, CallLikeOp):
                    unique_call_like_ops.add(e.op.name)

    print("\n\nPRINTING UNIQUE BUILD STRUCT OPS ")
    print(unique_build_struct_ops)
    print(f"total count is {len(unique_build_struct_ops)}")
    # Too many value ops, so I commented out printing them, but uncomment to get a sense of what they look like
    #print("\n\nPRINTING VALUE OPS")
    #print(unique_value_ops)
    print(f"total count of value ops is {len(unique_value_ops)}")
    print("\n\nPRINTING CALL LIKE OPS")
    print(unique_call_like_ops)
    print(f"total count is {len(unique_call_like_ops)}")


def main(dataflow_dialogues_dir: str, subsets: List[str], outdir: str):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    for subset in subsets:
        dataflow_dialogues = list(
            load_jsonl_file(
                data_jsonl=os.path.join(
                    dataflow_dialogues_dir, f"{subset}.dataflow_dialogues.jsonl"
                ),
                cls=Dialogue,
                unit=" dialogues",
            )
        )

        # Uncomment one of the following lines depending on which sort of experiment you want to run 

        #convert_lispress_to_python(dataflow_dialogues=dataflow_dialogues)
        #extract_library_functions(dataflow_dialogues=dataflow_dialogues)



def add_arguments(argument_parser: argparse.ArgumentParser) -> None:
    argument_parser.add_argument(
        "--dataflow_dialogues_dir", help="the dataflow dialogues data directory"
    )
    argument_parser.add_argument(
        "--subset", nargs="+", default=[], help="the subset to be analyzed"
    )
    argument_parser.add_argument("--outdir", help="the output directory")

if __name__ == "__main__":
    cmdline_parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter
    )
    add_arguments(cmdline_parser)
    args = cmdline_parser.parse_args()

    main(
        dataflow_dialogues_dir=args.dataflow_dialogues_dir,
        subsets=args.subset,
        outdir=args.outdir,
    )
