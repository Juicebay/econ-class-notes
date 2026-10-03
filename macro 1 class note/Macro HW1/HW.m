% ECON*6020 Assignment 1: Canadian business cycle statistics, 1976Q1-2026Q2
T = readtable("Assignment1_data.xlsx", Sheet="Combined", VariableNamingRule="preserve");

% ---- the ten series straight out of the file ------------------------------
output      = T.chained_2017_dollars_seasonally_adjusted_at_annual_rates_gross_domestic_product_at_market_prices;

consumption = T.chained_2017_dollars_seasonally_adjusted_at_annual_rates_semi_durable_goods ...
            + T.chained_2017_dollars_seasonally_adjusted_at_annual_rates_non_durable_goods ...
            + T.chained_2017_dollars_seasonally_adjusted_at_annual_rates_services;

investment  = T.chained_2017_dollars_seasonally_adjusted_at_annual_rates_non_residential_structures_machinery_and_equipment;

govcons     = T.chained_2017_dollars_seasonally_adjusted_at_annual_rates_general_governments_final_consumption_expenditure;

govinv      = T.chained_2017_dollars_seasonally_adjusted_at_annual_rates_general_governments_gross_fixed_capital_formation;

exports     = T.chained_2017_dollars_seasonally_adjusted_at_annual_rates_exports_of_goods_and_services;

imports     = T.chained_2017_dollars_seasonally_adjusted_at_annual_rates_less_imports_of_goods_and_services;

hours       = T.hours_worked_v4391505_quarterly_sum_hours;

pop         = T.population_v1_persons;

exrate      = 100 * T.exchange_rate_v37426_to_2016_v111666275_from_2017_quarterly_average_cad_per_usd;

% ---- the four you build ---------------------------------------------------
netexports   = 1 + (exports - imports) ./ output;

productivity = output ./ hours;

nominalGDP   = T.current_prices_seasonally_adjusted_at_annual_rates_gross_domestic_product_at_market_prices;
price        = 100 * nominalGDP ./ output;

% ---- capital stock: K(t+1) = I(t) + (1-delta) K(t), delta = 2.5% per quarter
% K(1976Q1) is set so that the average growth rates of capital and investment
% over the sample are identical -- bisection on K(1976Q1).
delta = 0.025;
K0lo = 1e11;  K0hi = 1e15;
gI   = mean(diff(log(investment)));
for it = 1:300
    K0 = sqrt(K0lo * K0hi);
    if mean(diff(log(capital(K0, investment, delta)))) > gI
        K0lo = K0;
    else
        K0hi = K0;
    end
end
K0 = sqrt(K0lo * K0hi);
K  = capital(K0, investment, delta);
fprintf("K(1976Q1) = %.4g   (K/Y = %.2f)   average growth K = %.4f%%  =  growth I = %.4f%%\n", ...
        K0, K0/output(1), 100*mean(diff(log(K))), 100*gI);

% ---- per-capita series: deflate the real quantities by population ----------
y  = output      ./ pop;   % real GDP per capita
c  = consumption ./ pop;   % consumption per capita
i  = investment  ./ pop;   % investment per capita
gc = govcons     ./ pop;   % gov't consumption expenditure per capita
gi = govinv      ./ pop;   % gov't investment expenditure per capita
ex = exports     ./ pop;   % exports per capita
im = imports     ./ pop;   % imports per capita
n  = hours       ./ pop;   % hours worked per capita
k  = K           ./ pop;   % capital stock per capita

% ---- already scale-free, so no population deflation ------------------------
nx   = netexports;   % 1 + (X - M)/Y   (a ratio)
w    = productivity; % labour productivity = output/hours (population cancels)
mpk  = output ./ K;  % capital productivity = output/capital stock
pgdp = price;        % price = GDP deflator (an index)

% ---- vector fed into the HP filter -----------------------------------------
% column order follows the table in the assignment:
%   1 y   2 c   3 i   4 gc  5 gi  6 ex  7 im  8 nx  9 n  10 w
%  11 k  12 mpk  13 exrate  14 pgdp
a = [y, c, i, gc, gi, ex, im, nx, n, w, k, mpk, exrate, pgdp];   % 202 x 14

% ---- date labels for the figures (grab them before the filter section) -----
q  = string(T.quarter);                                              % "1976Q1" ... "2026Q2"
ty = double(extractBefore(q,5)) + (double(extractAfter(q,"Q"))-1)/4; % decimal year axis

% ---- HP filter: the block from hpfilter.m, applied to our 'a' --------------
lambda = 1600;
[T,nvar] = size(a);                                   % T = number of periods
d = (1+6*lambda)*ones(T,1);
x = diag(d);
d = -4*lambda*ones(T-1,1);
x = x + diag(d,1) + diag(d,-1);
d = lambda*ones(T-2,1);
x = x + diag(d,2) + diag(d,-2);
x(1,1) = 1+lambda;
x(1,2) = -2*lambda;
x(2,1) = -2*lambda;
x(2,2) = 1+5*lambda;
x(T,T) = 1+lambda;
x(T-1,T) = -2*lambda;
x(T,T-1) = -2*lambda;
x(T-1,T-1) = 1+5*lambda;
hpmat = inv(x);                                       % matrix to apply HP filter
raw = log(a);                                         % raw = logged data series
hptrend = hpmat*raw;                                  % HP trend line
hpdata = raw - hptrend;                               % deviation from HP trend
vcv = (hpdata'*hpdata)/T;                             % variance-covariance matrix
var = sum(vcv .* eye(nvar,nvar));                     % variance (vector)
sd = sqrt(var)*100;                                   % std. deviation (vector)
corr = vcv ./ sqrt(var'*var);                         % corr (matrix)

% autocorrelation of output: a measure of persistence
yhp = hpdata(2:T,1);              % for periods 2:T
yhplag = hpdata(1:T-1,1);         % for periods 1:T-1
autoy = corrcoef(yhp, yhplag);

% ---- question 1: the statistics ---------------------------------------------
varnames = ["Output"; "Consumption"; "Investment"; "Gov consumption"; ...
            "Gov investment"; "Exports"; "Imports"; "Net exports"; ...
            "Hours worked"; "Labour productivity"; "Capital"; ...
            "Capital productivity"; "Nominal exchange rate"; "Price"];
fprintf("\n%-22s %8s %8s\n", "variable", "sd (%)", "corr(y)");
for j = 1:nvar
    fprintf("%-22s %8.2f %8.2f\n", varnames(j), sd(j), corr(j,1));
end
fprintf("\ncorr(hours worked, labour productivity) = %+.4f\n", corr(9,10));
fprintf("corr(hours worked, capital productivity) = %+.4f\n", corr(9,12));
fprintf("autocorrelation of output = %.3f\n", autoy(1,2));

% ======================= question 2: GDP and price ==========================
% column 1 of raw/hptrend/hpdata is GDP per capita; column 14 is the price
% (GDP deflator). raw = logged series, hptrend = trend, hpdata = cycle.
cyc = 100*hpdata;

% ---- 2a: per variable, data + trend on top, the cycle below ----------------
figure
subplot(2,1,1)
plot(ty, raw(:,1)); hold on
plot(ty, hptrend(:,1))
title("GDP per capita: data and HP trend"); legend("log data","HP trend","Location","northwest"); grid on
subplot(2,1,2)
plot(ty, cyc(:,1))
yline(0, ':'); grid on
title("GDP per capita: cycle"); xlabel("year"); ylabel("% from trend")
exportgraphics(gcf, "q2_gdp.png", "Resolution", 150)

figure
subplot(2,1,1)
plot(ty, raw(:,14)); hold on
plot(ty, hptrend(:,14))
title("Price (GDP deflator): data and HP trend"); legend("log data","HP trend","Location","northwest"); grid on
subplot(2,1,2)
plot(ty, cyc(:,14))
yline(0, ':'); grid on
title("Price (GDP deflator): cycle"); xlabel("year"); ylabel("% from trend")
exportgraphics(gcf, "q2_price.png", "Resolution", 150)

% ---- 2b/2c: turning points of the three recessions -------------------------
% in each window: the last cycle peak = start of the recession, the trough =
% start of the recovery; depth and peak-to-trough quarters measure severity,
% and the run of quarters spent below trend measures how slow the recovery was
labels = ["early 1980s    "; "early 1990s    "; "Great Recession"];
wlo    = [1980 1988.5 2007];          % 1988.5 = 1988Q3: the 1988Q2 spike (+2.56)
whi    = [1984 1993   2011];          % is within 0.01pp of the 1989Q1 peak (+2.55)
for ww = 1:3
    win = find(ty >= wlo(ww) & ty <= whi(ww));
    [pk, a1] = max(cyc(win,1));  [tr, b1] = min(cyc(win,1));
    tpk = win(a1);  ttr = win(b1);
    back = ttr - 1 + find(cyc(ttr:end,1) >= 0, 1);       % first quarter back at/above trend
    below = sum(cyc(tpk+1:back-1,1) < 0);                % quarters spent below trend
    fprintf("%s: peak %s (%+.2f%%)  trough %s (%+.2f%%)  depth %+.2f%%  %d quarters peak->trough, %d quarters below trend (back at trend %s)\n", ...
            labels(ww), q(tpk), pk, q(ttr), tr, tr, ttr-tpk, below, q(back));
end

% ======================= question 3: cause ==================================
% evidence: the price cycle also falls below trend during the recession
% (output down and price down = demand shock, not a supply shock)
c07 = corrcoef(cyc(ty>=2007 & ty<=2011,1), cyc(ty>=2007 & ty<=2011,14));  c07 = c07(1,2);
c7983 = corrcoef(cyc(ty>=1979 & ty<=1983,1), cyc(ty>=1979 & ty<=1983,14)); c7983 = c7983(1,2);
c7982 = corrcoef(cyc(ty>=1979 & ty<=1982,1), cyc(ty>=1979 & ty<=1982,14)); c7982 = c7982(1,2);
w08 = find(ty >= 2008 & ty <= 2010.75);
[lo, m1] = min(cyc(w08,14));
fprintf("\ncorr(output cycle, price cycle), 2007Q1-2011Q4 = %+.3f\n", c07);
fprintf("price cycle minimum 2008-2010: %+.2f%% in %s\n", lo, q(w08(m1)));
fprintf("corr(output cycle, price cycle), 1979Q1-1983Q4 = %+.3f\n", c7983);
fprintf("   (same correlation over 1979Q1-1982Q4 only: %+.3f -- in 1979-80 the price\n", c7982);
fprintf("    cycle was still below trend, so the window has to end in 1983)\n");

% ======================= question 4: coronavirus ============================
% the hit: % change from 2019Q4 (last quarter before the pandemic) to the
% 2020Q2 trough, the cycle low within 2020, and when each series got back
% to its 2019Q4 level
cols  = [1 14 9];                     % output, price, hours worked
names = ["output", "price", "hours"];
k19 = find(q == "2019Q4");            % last pre-pandemic quarter
k20 = find(q == "2020Q2");            % pandemic trough quarter
fprintf("\n%-7s %10s %10s %12s %18s\n", "series", "log chg", "pct chg", "cycle low", "back at 2019Q4");
for cc = 1:3
    k = cols(cc);
    win = find(ty >= 2020 & ty <= 2020.75);             % the four 2020 quarters
    [lo, m1] = min(hpdata(win,k));                      % cycle low within 2020
    back = k20 - 1 + find(raw(k20:end,k) >= raw(k19,k), 1);
    fprintf("%-7s %9.2f%% %9.2f%% %11.2f%% %18s\n", names(cc), ...
            100*(raw(k20,k) - raw(k19,k)), 100*(exp(raw(k20,k) - raw(k19,k)) - 1), ...
            100*lo, q(back));
end

% ---- local function: iterate the capital law of motion ----------------------
function K = capital(K0, I, delta)
T = numel(I);
K = zeros(T,1);
K(1) = K0;
for t = 1:T-1
    K(t+1) = I(t) + (1-delta)*K(t);
end
end
