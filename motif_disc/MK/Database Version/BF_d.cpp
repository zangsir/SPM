/******************************************************************************
*******************************************************************************
******                                                                  *******
******     This code is written by Abdullah Al Mueen at the department  *******
******     of Computer Science and Engineering of University of         *******
******     California - RIverside.                                      *******
******                                                                  *******
*******************************************************************************
******************************************************************************/

/*#############################################################################
######                                                                  #######
######     This code is open to use, reuse and distribute at the user's #######
######     own risk and as long as the above credit is ON. The complete #######
######     description of the algorithm and methods applied can be      #######
######     found in the paper - EXACT DISCOVERY OF TIME SERIES MOTIFS   #######
######     by Abdullah Mueen, Eamonn Keogh and Qiang Zhu.               #######
######                                                                  #######
#############################################################################*/

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <signal.h>

#define INF        999999999999.0

FILE *fp;

double **data;
long long loc1 , loc2;

long long TIMESERIES;
int LENGTH;
double bsf;
double total = 0.0;
int abandon = 1;
    
/* Calculates the distance between two time series x and y. If the distance is
larger than the best so far (bsf) it stops computing and returns the approximate
distance. To get exact distance the bsf argument should be omitted.*/

double distance(double *x, double *y, int length , double best_so_far = INF )
{
    int i;
    double sum = 0;
    
    if( abandon == 1 )
    {
        double bsf2 = best_so_far*best_so_far;
        for ( i = 0 ; i < length && sum < bsf2  ; i++ )
            sum += (x[i]-y[i])*(x[i]-y[i]);
        return sqrt(sum);
    }
    else
    {
        for ( i = 0 ; i < length  ; i++ )
            sum += (x[i]-y[i])*(x[i]-y[i]);
        return sqrt(sum);
    }

}

/*Comparison function for qsort function. Compares two time series by using their
distances from the reference time series. */

void error(int id)
{
    if(id==1)
        printf("ERROR : Memory can't be allocated!!!\n\n");
    else if ( id == 2 )
        printf("ERROR : File not Found!!!\n\n");
    else if ( id == 3 )
        printf("ERROR : Can't create Output File!!!\n\n");
    else if ( id == 4 )
        printf("ERROR : Invalid Number of Arguments!!!\n\n");

    exit(1);

    }



void stop_exec(int sig)
{
    printf("Current Motif is (%lld",loc1);
    printf(",%lld)",loc2);
    printf(" and the distance is %lf\n",bsf);
    exit(1);
    }

    
int main(  int argc , char *argv[] )
{



    double d;
    long long i , j ;
    int  r = 0;
    double ex , ex2 , mean, std;
    long long length;
    int clear = 1;
    double t1,t2;
    int verbos = 0;

    /* taking inpput time series from the file in the data array and Normalizing
    them as well. */

    bsf = INF;
    i = 0;
    j = 0;
    ex = ex2 = 0;
    
    signal(SIGINT,stop_exec);
    t1 = clock();

    if(argc < 4 || argc > 6)
    {
        printf("Invalid number of arguments!!!");
        exit(1);
    }
    
    fp = fopen(argv[1],"r");
    TIMESERIES = atol(argv[2]);
    LENGTH = atoi(argv[3]);
    if( argc >= 5 )
        abandon = atoi(argv[4]);
    
    if( argc == 6 )
        verbos = atoi(argv[5]);

    if( verbos == 1 )
        printf("\nNumber of Time Series : %lld\nLength of Each Time Series : %d\n\n",TIMESERIES,LENGTH);


    data = (double **)malloc(sizeof(double *)*TIMESERIES);
    if( data == NULL  )
        error(1);
    data[0] = (double *)malloc(sizeof(double)*LENGTH);


    if( data[0] == NULL )
        error(1);

    while(fscanf(fp,"%lf",&d) != EOF && i < TIMESERIES)
    {
        data[i][j] = d;
        ex += d;
        ex2 += d*d;
        if( j == LENGTH - 1 )
        {
            mean = ex = ex/LENGTH;
            ex2 = ex2/LENGTH;
            std = sqrt(ex2-ex*ex);
            for( int k = 0 ; k < LENGTH ; k++ )
                data[i][k] = (data[i][k]-mean)/std;
            ex = ex2 = 0;
            i++;
            if( i != TIMESERIES )
                data[i] = (double *)malloc(sizeof(double)*LENGTH);
            if( data[i] == NULL )
                error(1);

            j = 0;
        }
        else
            j++;
    }

    fclose(fp);
    
    if(verbos == 1)
        printf("Data Have been Read and Normalized\n\n");

    for( i = 0 ; i < TIMESERIES; i++ )
        for( j = i+ clear; j < TIMESERIES ; j++ )
        {
            double x = distance(data[i],data[j],LENGTH,bsf);
            if( abandon == 0 )
                total += x;
            if( x == 0 ) continue;
            if( bsf > x )
            {
                bsf = x;
                loc1 = i;
                loc2 = j;
                if(verbos == 1)
                     printf("New best-so-far is %lf and (%lld , %lld) are the new motif pair\n",bsf,loc1,loc2);
                }
            }



        /*Printing section of the code.*/
        printf("\n\nFinal Motif is the pair ( %lld",loc1);
        printf(", %lld ) and the Motif distance is %lf\n\n",loc2,bsf);
        t2 = clock();
        if(verbos == 1)
        {
            printf("\nExecution Time was : %lf seconds\n",(t2-t1)/CLOCKS_PER_SEC);
            if(abandon == 0)
            {
                printf("Average Distance is %lf\n",((total/TIMESERIES)*(2.0/(TIMESERIES-1))));
                double sum = 0;
                for ( r = 0 ; r < 10 ; r++ )
                {
                    long long r_p = rand() % TIMESERIES;
                    double minVal = INF;
                    for( i = 0 ; i < TIMESERIES; i++ )
                         if( abs(i-r_p) >= clear )
                         {
                             double ll = distance( data[r_p] , data[i] , LENGTH );
                             if( ll < minVal )
                                 minVal = ll;
                         }

                    sum += minVal;
                }

                printf("Average nearest neighbor distance is %lf\n",sum/10);
            }
        }
}
